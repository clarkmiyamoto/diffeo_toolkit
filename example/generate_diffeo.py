from diffeo_toolkit.diffeo.diffeo_container import diffeo_container, sparse_diffeo_container

import torch

from datetime import datetime
import argparse
import json


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-xlength', type=int, required=True)
    parser.add_argument('--img-ylength', type=int, required=True)

    parser.add_argument('--diffeo-strengths', type=float, nargs='+', required=True, help='A list of float numbers (separated by space)')
    parser.add_argument('--diffeo-num', type=int, default=100, required=False)

    parser.add_argument('--name', type=str, default=None, required=False)
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    '''
    Generates g and g^{-1} with a given diffeo strength
    Saves results into '{filename}_grid.pt' and '{filename}_gridInverse.pt

    Example usage (in terminal):
    python generate_diffeo.py --img-xlength=224 --img-ylength=224 --diffeo-strengths=0.1 0.5 --diffeo-num=100
    '''

    ### Parse arguments
    args = parser()
    args_dict = vars(args)

    XLENGTH = args.img_xlength # int
    YLENGTH = args.img_ylength # int
    
    DIFFEO_STRENGTHS = args.diffeo_strengths # list[floats]
    DIFFEO_NUM = args.diffeo_num # int
    DIFFEO_XCUT = 4
    DIFFEO_YCUT = 4
    DIFFEO_TERMS = 3
    
    NAME = args.name
    if NAME == None:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = current_time
    else:
        filename = NAME

    ### CODE
    # Torch parameters
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    print(f"Using device: {device}")

    # Generate diffeos (g)
    SparseDiffeoContainer = sparse_diffeo_container(XLENGTH, 
                                                    YLENGTH, 
                                                    device=device)
    for strength in DIFFEO_STRENGTHS:
        SparseDiffeoContainer.sparse_AB_append(x_cutoff=DIFFEO_XCUT, 
                                               y_cutoff=4, 
                                               num_of_terms=DIFFEO_YCUT, 
                                               diffeo_amp=strength,
                                               num_of_diffeo=DIFFEO_NUM)
    SparseDiffeoContainer.get_all_grid()
    SparseDiffeoContainer.to(device)

    # Get grid samples
    grid_sample = torch.cat(SparseDiffeoContainer.diffeos)
    grid_sample_inverse = torch.cat(SparseDiffeoContainer.get_inverse_grid(mode='bilinear', align_corners=True).diffeos)

    # Save files
    torch.save(grid_sample, filename + '_grid.pt')
    torch.save(grid_sample_inverse, filename + '_gridInverse.pt')

    with open(filename + '_args.json', 'w') as json_file:
        json.dump(args_dict, json_file, indent=4)

    # Example usage of `grid_sample` object:
    #
    # val_image, _  = torch.utils.data.DataLoader(<DATSET OBJ>, batch_size = 1)
    # image = val_image.repeat(len(DIFFEO_STRENGTHS) * DIFFEO_NUM,1,1,1).to(device)
    # torch.nn.functional.grid_sample(image, grid_sample)