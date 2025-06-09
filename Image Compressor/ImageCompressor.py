import cv2
import numpy as np
import os

class ImageCompressor(object):
    """Inputs : original_path - folder with images to be compressed;
                compression_path - folder for compressed images (optional)"""
    def __init__(self,original_path,compression_path=None):
        self.original_path = original_path
        self.compression_path = compression_path
        
    def BlockAveraging(self,image_filename):
        """Method for image compression based on Block Averaging Algorithm"""
        N = 3
        pixel_matrix = cv2.imread(self.original_path+image_filename)
        l_lim,w_lim,c_lim = list(pixel_matrix.shape)
        pixel_matrix = cv2.split(pixel_matrix)
        #Divide picture into equal blocks (N by N size)
        for channel in range(len(pixel_matrix)):
            block_y_coord,block_x_coord = [0,0]
            while block_y_coord + N <= l_lim:
                block_x_coord = 0
                while block_x_coord + N <= w_lim:
                    #Take the average color value of each block and substitute values around the block by the average.
                    pixel_matrix[channel][block_y_coord:block_y_coord + N,block_x_coord:block_x_coord + N] = round(np.mean(pixel_matrix[channel][block_y_coord:block_y_coord + N,block_x_coord:block_x_coord + N]))
                    block_x_coord+=N
                block_y_coord+=N

        merged = cv2.merge(np.array(pixel_matrix))
        #Save it
        cv2.imwrite(self.compression_path+"\\"+image_filename,merged)
        
    def main(self):
        self.original_path+="\\"
        #Getting the list of filenames only with .jpg,.png and .jpeg extensions
        original_files = [filename for filename in os.listdir(self.original_path) if filename.split('.')[len(filename.split('.'))-1] in ['jpg','png','jpeg']]
        #If a path for saving compressed pictures were not specified, create nested directory inside of the directory with original files.
        if self.compression_path is None:
            self.compression_path = self.original_path+"Compression_Folder"
        if not os.path.exists(self.compression_path):
            os.mkdir(self.compression_path)
        #Compressing pictures
        for filename in original_files:
            self.BlockAveraging(filename)
        return 0

if __name__=='__main__':
    ImageCompressor("path with pictures to be compressed. Use '\\' instead of '\'","path for compressed pictures (optional). Use '\\' instead of '\'").main()
