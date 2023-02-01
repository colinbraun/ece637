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
    int numConPixels = 0;
    Pixel startPoint = {.m = 67, .n = 45};
    double T = 3;
    int classLabel = 1;
    ConnectedSet(startPoint, T, input_img.mono, input_img.width, input_img.height, classLabel, seg, &numConPixels);
    // Flip colors of images
    for (int row = 0; row < input_img.height; row++) {
        for (int col = 0; col < input_img.width; col++) {
            if (seg[row][col] == 0)
                seg[row][col] = 255;
            else if (seg[row][col] == classLabel)
                seg[row][col] = 0;
        }
    }
    save_grayscale_image_to_tiff_i(seg, input_img.width, input_img.height, "connected-set-3t.tif");
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
