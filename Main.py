from Futoshiki import FutoMain
from Skyscrapper import SkyMain


FUTO_DATA = "test_futo_4_0.txt"
SKY_DATA = "test_sky_4_0.txt"


if __name__ == '__main__':
    # FutoMain.start_backtracking(FUTO_DATA)
    # FutoMain.start_forward_checking(FUTO_DATA)

    # SkyMain.start_backtracking(SKY_DATA)
    SkyMain.start_forward_checkin(SKY_DATA)
