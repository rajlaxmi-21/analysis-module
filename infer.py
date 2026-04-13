#!/usr/bin/env python

import os, sys, argparse, warnings
#sys.path.append('/content/SR/src')

# to switch between S2DR3 (super-resolution) and S2DR4 (super-resolution & cloud mitigation) switch between s2dr3.inferutils and s2dr4.inferutils in the code below.
# !! where cloud mitigation is not necessary S2DR3 is recommended over S2DR4
from s2dr3.inferutils import infer

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', type=str, default='/home/ubuntu/s2dr3/data', help='Input image or folder')
    parser.add_argument('--savepath', type=str, default='/home/ubuntu/s2dr3/output', help='Output image or folder')
    parser.add_argument('--logpath', type=str, default='/home/ubuntu/s2dr3/logs', help='Path for logging')
    parser.add_argument('-f', '--force', action='store_true', help="force reprocessing")
    parser.add_argument('-g', '--coreg', action='store_true', help="georeference fo ESRI basmap")
    #parser.add_argument('-d', '--debug', action='store_true', help='print debugging messages')
    parser.add_argument('-q', '--quiet', action='store_true', help='run quiet')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose outout')
    parser.add_argument('-s', '--simulate', action='store_true', help='process a small simulation patch')
    parser.add_argument('-p', '--make_preview', action='store_true', help='Generate and publish preview')
    parser.add_argument('-c', '--cogs', action='store_true', help='Generate COGs outputs RGB/IRP/NDVI')
    parser.add_argument('--date', type=str, default=None, help='Date')
    parser.add_argument('--date_range', type=int, default=7, help='Date range')
    parser.add_argument('--max_clouds', type=int, default=0, help='Maximum cloud cover')
    parser.add_argument('--b10m10', type=str, default=None, help='Direct path of the input S2L2A 10-band image')
    parser.add_argument('--aoi', nargs='+', default=None, help='AOI')
    parser.add_argument('--geojson', type=str, default=None, help='GeoJSON input')
    parser.add_argument('--mgrs', type=str, default=None, help='MGRS tile')
    parser.add_argument('--s2id', type=str, default=None, help='Exact S2 catalogue ID')
    parser.add_argument('--iso', type=str, default=None, help='Country 2-digit ISO code')
    parser.add_argument('--NM', nargs='+', default=None, help='Indices of MGRS subsubtile [0..9 0..9]')
    parser.add_argument('--UV', nargs='+', default=None, help='Indices of MGRS subtile [0..2 0..2]')
    parser.add_argument('--bands_out', nargs='+', default=None, help='Spectral bands to generate in Sentinel-2 notation')
    parser.add_argument('--tile', type=int, default=640, help='Size of the processing tile')
    parser.add_argument('-b', '--batch', type=int, default=1, help='Batch size (only b=1 is supported)')

    args = parser.parse_args()

    args.uid, args.org = "66546448", "nnmahangare@dypcoeakurdi.ac.in"

    if args.aoi is not None: args.aoi = [float(x) for x in args.aoi]
    if args.NM is not None: args.NM = [int(x) for x in args.NM]
    if args.UV is not None: args.UV = [int(x) for x in args.UV]
    if args.bands_out is None or args.make_preview: 
        args.bands_out = 'B02 B03 B04 B05 B06 B07 B08 B8A B11 B12'.split()
    args.verbose = False
    os.makedirs(args.logpath, exist_ok=True)

    infer(args)

if __name__ == '__main__':
    main()
