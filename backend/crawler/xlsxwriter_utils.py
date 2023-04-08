import xlsxwriter
from io import BytesIO
from django.db.models import Sum
from .models import Loan


def create_workbook():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    return workbook, output


def create_formats(workbook):
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'bg_color': '#4CAF50',  # Green background color
        'font_color': 'white',  # White text
        'border': 1,
        'border_color': 'black',
    })

    body_format = workbook.add_format({
        'align': 'left',
        'font_size': 12,
        'border': 1,
        'border_color': 'black',
        'text_wrap': True,  # Wraps long text
    })

    currency_format = workbook.add_format({
        'align': 'center',
        'font_size': 12,
        'border': 1,
        'border_color': 'black',
    })

    return header_format, body_format, currency_format


def write_data_sheet(workbook, header_format, body_format, currency_format):
    data_sheet = workbook.add_worksheet('Data sheet')
    headers = ['Borrower', 'Amount', 'Currency', 'Country', 'Sector', 'Year']

    for col_num, header in enumerate(headers):
        data_sheet.write(0, col_num, header, header_format)

    loans = Loan.objects.all()
    for row_num, loan in enumerate(loans):
        data_sheet.write(row_num + 1, 0, loan.borrower, body_format)
        data_sheet.write(row_num + 1, 1, float(loan.amount), body_format)
        data_sheet.write(row_num + 1, 2, loan.currency, currency_format)  # Use the currency_format
        data_sheet.write(row_num + 1, 3, loan.country.name, body_format)
        data_sheet.write(row_num + 1, 4, loan.sector.name, body_format)
        data_sheet.write(row_num + 1, 5, loan.year, body_format)

    data_sheet.set_column(0, 0, 35)  # Borrower
    data_sheet.set_column(1, 1, 10)  # Amount
    data_sheet.set_column(2, 2, 10)  # Currency
    data_sheet.set_column(3, 3, 15)  # Country
    data_sheet.set_column(4, 4, 15)  # Sector
    data_sheet.set_column(5, 5, 5)   # Year

    return data_sheet


def write_aggregated_sheets(workbook, header_format):
    year_sheet, sector_sheet, country_sheet = create_aggregated_sheets(workbook)
    write_year_data(year_sheet, header_format)
    write_sector_data(sector_sheet, header_format)
    write_country_data(country_sheet, header_format)
    return year_sheet, sector_sheet, country_sheet


def create_aggregated_sheets(workbook):
    year_sheet = workbook.add_worksheet('By Year')
    sector_sheet = workbook.add_worksheet('By Sector')
    country_sheet = workbook.add_worksheet('By Country')

    year_sheet.hide()
    sector_sheet.hide()
    country_sheet.hide()

    return year_sheet, sector_sheet, country_sheet


def write_year_data(year_sheet, header_format):
    year_data = (
        Loan.objects.values('year')
        .annotate(total_amount=Sum('amount'))
        .order_by('year')
    )

    year_sheet.write(0, 0, 'Year', header_format)
    year_sheet.write(0, 1, 'Total Amount', header_format)

    for row_num, data in enumerate(year_data):
        year_sheet.write(row_num + 1, 0, data['year'])
        year_sheet.write(row_num + 1, 1, float(data['total_amount']))


def write_sector_data(sector_sheet, header_format):
    sector_data = (
        Loan.objects.values('sector__name')
        .annotate(total_amount=Sum('amount'))
        .order_by('sector__name')
    )
    sector_sheet.write(0, 0, 'Sector', header_format)
    sector_sheet.write(0, 1, 'Total Amount', header_format)

    for row_num, data in enumerate(sector_data):
        sector_sheet.write(row_num + 1, 0, data['sector__name'])
        sector_sheet.write(row_num + 1, 1, float(data['total_amount']))


def write_country_data(country_sheet, header_format):
    country_data = (
    Loan.objects.values('country__name')
    .annotate(total_amount=Sum('amount'))
    .order_by('country__name')
    )
    country_sheet.write(0, 0, 'Country', header_format)
    country_sheet.write(0, 1, 'Total Amount', header_format)

    for row_num, data in enumerate(country_data):
        country_sheet.write(row_num + 1, 0, data['country__name'])
        country_sheet.write(row_num + 1, 1, float(data['total_amount']))


def write_chart_sheet(workbook, header_format, year_sheet, sector_sheet, country_sheet):
    chart_sheet = create_chart_sheet(workbook)
    helper_sheet = create_helper_sheet(workbook)
    write_helper_formulas(helper_sheet, year_sheet, sector_sheet, country_sheet)
    dynamic_chart = create_dynamic_chart(workbook, helper_sheet)
    chart_sheet.insert_chart('A3', dynamic_chart)
    return chart_sheet


def create_chart_sheet(workbook):
    chart_sheet = workbook.add_worksheet('Chart sheet')
    chart_sheet.write('A1', "Select aggregation type in the dropdown menu in cell A2.")

    # Create a format for the dropdown cell
    dropdown_format = workbook.add_format({'bg_color': 'yellow', 'font_color': 'red'})

    # Add data validation with the format
    chart_sheet.data_validation('A2', {'validate': 'list',
                                       'source': ['Year', 'Sector', 'Country'],
                                       })

    # Write an empty string to cell A2 to apply the format
    chart_sheet.write('A2', '', dropdown_format)

    return chart_sheet


def create_helper_sheet(workbook):
    helper_sheet = workbook.add_worksheet('Helper')
    helper_sheet.hide()
    return helper_sheet


def write_helper_formulas(helper_sheet, year_sheet, sector_sheet, country_sheet):
    max_rows = max(year_sheet.dim_rowmax, sector_sheet.dim_rowmax, country_sheet.dim_rowmax)
    for i in range(max_rows):
        helper_sheet.write_formula('A{}'.format(i + 1),
                                   '=IF(\'Chart sheet\'!$A$2="Year", IF(\'By Year\'!B{}>0, \'By Year\'!A{}, ""), IF(\'Chart sheet\'!$A$2="Sector", IF(\'By Sector\'!B{}>0, \'By Sector\'!A{}, ""), IF(\'By Country\'!B{}>0, \'By Country\'!A{}, "")))'.format(
                                       i + 1, i + 1, i + 1, i + 1, i + 1, i + 1))
        helper_sheet.write_formula('B{}'.format(i + 1),
                                   '=IF(\'Chart sheet\'!$A$2="Year", IF(\'By Year\'!B{}>0, \'By Year\'!B{}, ""), IF(\'Chart sheet\'!$A$2="Sector", IF(\'By Sector\'!B{}>0, \'By Sector\'!B{}, ""), IF(\'By Country\'!B{}>0, \'By Country\'!B{}, "")))'.format(
                                       i + 1, i + 1, i + 1, i + 1, i + 1, i + 1))


def create_dynamic_chart(workbook, helper_sheet):
    dynamic_chart = workbook.add_chart({'type': 'column'})
    dynamic_chart.add_series({
    'name': '=Helper!$B$1',
    'categories': '=Helper!$A$2:$A${}'.format(helper_sheet.dim_rowmax + 1),
    'values': '=Helper!$B$2:$B${}'.format(helper_sheet.dim_rowmax + 1),
    })
    dynamic_chart.set_title({'name': 'Aggregated Data'})
    dynamic_chart.set_x_axis({'name': '=Chart!$A$2'})
    dynamic_chart.set_y_axis({'name': 'Value'})

    return dynamic_chart


def save_excel_file(workbook, output):
    workbook.close()
    with open("loan-summary.xlsx", "wb") as output_file:
        output_file.write(output.getvalue())
