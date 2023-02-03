#include <math.h>
#include <tiff.h>
#include <allocate.h>
#include <randlib.h>
#include <typeutil.h>
#include "util.h"

void error(char *name);

int main(int argc, char **argv)
{
    FILE *fp;
    struct TIFF_img input_img;

    char *fileName = "img22gd2.tif";
    if ((fp = fopen(fileName, "rb")) == NULL)
    {
        fprintf(stderr, "cannot open file %s\n", fileName);
        exit(1);
    }

    /* read image */
    if (read_TIFF(fp, &input_img))
    {
        fprintf(stderr, "error reading file %s\n", fileName);
        exit(1);
    }

    /* close image file */
    fclose(fp);

    /* check the type of image data */
    char imageType = 'g';
    if (input_img.TIFF_type != imageType)
    {
        fprintf(stderr, "error:  Wrong image type\n");
        exit(1);
    }

    unsigned int **seg = (unsigned int **)get_img(input_img.width, input_img.height, sizeof(unsigned int));
    
    unsigned int **result = (unsigned int **)get_img(input_img.width, input_img.height, sizeof(unsigned int));
    int labelsWithLargeSegments[256];
    int classLabel = 0;
    int largeSegCount = 0;
    double T = 1;
    for (int row = 0; row < input_img.height; row++) {
        for (int col = 0; col < input_img.width; col++) {
            if (seg[row][col] == 0) {
                classLabel++;
                int numConPixels = 0;
                Pixel startPoint = {.m = row, .n = col};
                ConnectedSet(startPoint, T, input_img.mono, input_img.width, input_img.height, classLabel, seg, &numConPixels);
                if (numConPixels > 100) {
                    labelsWithLargeSegments[largeSegCount] = classLabel;
                    largeSegCount++;
                    printf("Label %d had more than 100 connected pixels\n", classLabel);
                }
            }
        }
    }
    // Set all segments that are not larger than 100 pixels to 0
    for (int row = 0; row < input_img.height; row++) {
        for (int col = 0; col < input_img.width; col++) {
            unsigned int label = seg[row][col];
            unsigned int labelIsLarge = 0;
            int i;
            for (i = 0; i < largeSegCount; i++) {
                if (label == labelsWithLargeSegments[i]) {
                    labelIsLarge = 1;
                    break;
                }
            }
            if (labelIsLarge) {
                result[row][col] = i+1;
            }
        }
    }
    save_grayscale_image_to_tiff_i(result, input_img.width, input_img.height, "segmentation-1t.tif");
    printf("Segmentation done\n");
    printf("Total Number of Segments: %d\n", classLabel);
    printf("Number of Large Segments: %d\n", largeSegCount);
}


void error(char *name)
{
    printf("usage:  %s  image.tiff \n\n", name);
    printf("this program reads in a 24-bit color TIFF image.\n");
    printf("It then horizontally filters the green component, adds noise,\n");
    printf("and writes out the result as an 8-bit image\n");
    printf("with the name 'green.tiff'.\n");
    printf("It also generates an 8-bit color image,\n");
    printf("that swaps red and green components from the input image");
    exit(1);
}
