from django.core.management.base import BaseCommand

from crawler.xlsxwriter_utils import create_workbook, create_formats, write_data_sheet, write_aggregated_sheets, \
    write_chart_sheet, save_excel_file


class Command(BaseCommand):
    help = 'Download an Excel file with loan data and save it locally.'

    def handle(self, *args, **options):
        workbook, output = create_workbook()

        header_format, body_format, currency_format = create_formats(workbook)

        write_data_sheet(workbook, header_format, body_format, currency_format)

        year_sheet, sector_sheet, country_sheet = write_aggregated_sheets(workbook, header_format)

        write_chart_sheet(workbook, header_format, year_sheet, sector_sheet, country_sheet)

        save_excel_file(workbook, output)

        self.stdout.write(self.style.SUCCESS('Excel file saved as "as-scan-summary.xlsx".'))
