import logging
import os
from datetime import datetime


def setup_logger():
    # ایجاد پوشه لاگ‌ها اگر وجود ندارد
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # نام فایل بر اساس تاریخ
    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

    # تنظیمات لاگ‌گیری
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


logger = setup_logger()