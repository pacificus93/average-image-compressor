import cv2
import numpy as np
import os

class ImageCompressor(object):
    """Inputs : original_path - folder with images to be compressed; compression_path - folder for compressed images (to be automatically created later using main() function)"""
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
        
        for channel in range(len(channels_compressed)):
            block_y_coord,block_x_coord = [0,0]
            while block_y_coord + block_side_length <= l_lim:
                block_x_coord = 0
                row = []
                while block_x_coord + block_side_length <= w_lim:
                    row.append(round(np.mean(pixel_matrix_split_to_channels[channel][block_y_coord:block_y_coord + block_side_length,
                                                                                     block_x_coord:block_x_coord + block_side_length]
                                             )
                                     )
                               )
                    block_x_coord+=block_side_length
                channels_compressed[channel].append(row)
                block_y_coord+=block_side_length

        merged = cv2.merge(np.array(channels_compressed))
        cv2.imwrite(self.compression_path+image_filename,merged)
        
    def main(self):
        
        #Getting the list of filenames only with .jpg,.png and .jpeg extensions
        original_files = [filename for filename in os.listdir(self.original_path) if filename.split('.')[len(filename.split('.'))-1] in ['jpg','png','jpeg']]
        
        #Avoid creating folder for compressioned pictures, if already exists
        if "Compression_Folder" not in [name for name in os.listdir(self.original_path)]:
            os.mkdir(self.original_path+"Compression_Folder")
        
        self.compression_path = self.original_path+"Compression_Folder\\"

        for filename in original_files:
            if filename not in os.listdir(self.original_path+"Compression_Folder\\"):
                self.BlockAveraging(filename)
        return 0

if __name__=='__main__':
    ImageCompressor("LocationOfTheFolderWithImageToBeCompressed").main()
