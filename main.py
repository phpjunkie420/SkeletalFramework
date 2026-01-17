from pathlib import Path

from skeletal_framework._error_handling import ExceptionHandlerDialog

if __name__ == '__main__':

    dialog = ExceptionHandlerDialog(
        OSError,
        Path(r'C:\Users\phpjunkie\Python\SkeletalFramework\crash_reports\12-31-2025 11.39.39.log').read_text(encoding = 'utf-8')
    )
    dialog.show_window()
