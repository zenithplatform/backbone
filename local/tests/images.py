__author__ = 'civa'

from processors import fits as FP

def main():
    fp = FP.FITSProcessor()
    fp.open("D:\\Programming\\Astronomy\\Dev\\SampleFiles\\gll_iem_v02_P6_V11_DIFFUSE.fit")
    fp.get_image()

if __name__ == "__main__":
    main()