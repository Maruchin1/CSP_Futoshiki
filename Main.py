from Futoshiki import FutoMain
from Skyscrapper import SkyMain


FUTO_DATA = "test_futo_4_0.txt"
SKY_DATA = "test_sky_6_4.txt"


if __name__ == '__main__':
    # FutoMain.start_backtracking(file_name=FUTO_DATA)
    # FutoMain.start_forward_checking(file_name=FUTO_DATA)

    # SkyMain.start_backtracking(file_name=SKY_DATA, reduce_fields_enabled=True)
    SkyMain.start_forward_checkin(file_name=SKY_DATA, reduce_fields_enabled=False)
