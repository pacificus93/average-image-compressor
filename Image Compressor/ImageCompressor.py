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
        block_side_length = 4
        pixel_matrix = cv2.imread(self.original_path+image_filename)
        l_lim,w_lim,c_lim = list(pixel_matrix.shape)
        pixel_matrix_split_to_channels = cv2.split(pixel_matrix)
        
        channels_compressed = [[],[],[]]

        #Divide picture into 4 by 4 pixel blocks
        for channel in range(len(channels_compressed)):
            block_y_coord,block_x_coord = [0,0]
            while block_y_coord + block_side_length <= l_lim:
                block_x_coord = 0
                row = []
                while block_x_coord + block_side_length <= w_lim:
                    #Take the average color of each block.
                    #Create the pixel matrix, with the entry values, according to the relative block location.
                    row.append(round(np.mean(pixel_matrix_split_to_channels[channel][block_y_coord:block_y_coord + block_side_length,
                                                                                     block_x_coord:block_x_coord + block_side_length]
                                             )
                                     )
                               )
                    block_x_coord+=block_side_length
                channels_compressed[channel].append(row)
                block_y_coord+=block_side_length

        merged = cv2.merge(np.array(channels_compressed))
        #Save it
        cv2.imwrite(self.compression_path+"\\"+image_filename,merged)
        
    def main(self):
        self.original_path+="\\"
        #Getting the list of filenames only with .jpg,.png and .jpeg extensions
        original_files = [filename for filename in os.listdir(self.original_path) if filename.split('.')[len(filename.split('.'))-1] in ['jpg','png','jpeg']]
        #If a path for compressed pictures is not mentioned, create Compression_Folder inside of the path with the original pictures
        if self.compression_path is None:
            self.compression_path = self.original_path+"Compression_Folder"
        #Сreate folder for compressioned pictures, if it doesn't exist
        if not os.path.exists(self.compression_path):
            os.mkdir(self.compression_path)
        #Compressing pictures
        for filename in original_files:
            if filename not in os.listdir(self.compression_path + "\\"):
                self.BlockAveraging(filename)
        return 0

if __name__=='__main__':
    ImageCompressor("original pictures pathway","pathway for compressed pictures (optional)").main()
