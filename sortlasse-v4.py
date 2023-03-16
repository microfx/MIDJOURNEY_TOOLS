from sewar.full_ref import rmse
import imageio
import numpy as np
from pathlib import Path
import time
import argparse
import os
from tqdm.auto import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('-i', action='store_true')
    parser.add_argument('-o')
    parser.add_argument('-c', action='store_true')
    args = parser.parse_args()
    path = Path(args.path)

    start = time.time()  #start timer to measure to time the script took (for one iteration)
    pictures = []
   # print(f"printing from .py pictures array {pictures}") it's empty now obviously

    if path.is_dir():
        for file in path.iterdir():
            if not file.is_file():
                continue
            pictures.append(imageio.imread(file))
    else:
        file_name = path.name
        parent_directory = path.parent
        parent_directory = sorted(parent_directory, key=lambda x: os.path.basename(x))  
        pictures.append(imageio.imread(path))
        for file in parent_directory.iterdir():
            if not file.is_file() or file.name == file_name or file.name[0] == '.':
                continue
            pictures.append(imageio.imread(file))  
    pictures = greedy_hamilton_circle(pictures)
    if args.i:
        pictures = interpolate(pictures)
    if args.c:
        imageio.mimsave(args.o, pictures, duration=0.2)
    else:
        if not os.path.exists(args.o):
            os.mkdir(args.o)
        for i, image in tqdm(enumerate(pictures), total=len(pictures), ncols=100, colour='blue', desc='| Images moved'):
           tqdm.write(f"| writing images to new subfolder: {args.o}/{i:03}.png")
           imageio.imwrite(f"{args.o}/{i:03}.png", image)
    stop = time.time()
    elapsed_time = stop - start
    elapsed_time = round(elapsed_time, 2)
    print(f"| the script took {elapsed_time} seconds in {path}")

def image_similarity(image_1, imgage_2):
    return rmse(image_1, imgage_2)

def calculate_distance_matrix(pictures):
    matrix = np.ones((len(pictures), len(pictures)))
    for i in range(len(pictures)):
        for j in range (i+1, len(pictures)):
            matrix[i,j] = image_similarity(pictures[i], pictures[j])
            matrix[j,i] = matrix[i,j]
    return matrix


def greedy_hamilton_circle(pictures):
    distances = calculate_distance_matrix(pictures)
    visited = set()
    visited.add(0)
    ordered_pictures = [(0,pictures[0])]
    while len(visited) < len(pictures):
        next_image = None
        similarities = distances[ordered_pictures[-1][0]]
        similarities = [(i, similarities[i]) for i in range(len(similarities))]
        similarities = sorted(similarities, key=lambda x: x[1])
        for index, similarity in similarities:
            if not index in visited:
                visited.add(index)
                next_image = pictures[index]
                ordered_pictures.append((index, next_image))
                break
    print('┌───────────────────────────────────┐')
    print(f'│ NEW ORDER:')
    print('└───────────────────────────────────┘')            
    print([x[0] for x in ordered_pictures])
    print('')
    return [x[1] for x in ordered_pictures]

def average (image_1, image_2=None):
    img_1 = np.asarray(image_1)
    img_2 = np.asarray(image_2)
    avg = np.mean([img_1, img_2], axis=0)
    return imageio.core.util.Image(avg)


def interpolate(pictures, threshold=10):
    i = 0
    while i < len(pictures) - 1:
        if image_similarity(pictures[i], pictures[i+1]) > threshold:
            interp = average(pictures[i], pictures[i+1])
            pictures.insert(i+1, interp)
        else:
            i += 1
    print(len(pictures))
    return pictures

if __name__ == '__main__':
    main()

