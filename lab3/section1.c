#include <math.h>
#include <tiff.h>
#include <allocate.h>
#include <randlib.h>
#include <typeutil.h>
#include "util.h"

typedef struct pixel
{
    int m, n; /* m=row, n=col */
} Pixel;

void error(char *name);

void ConnectedNeighbors(
    Pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int *M,
    Pixel c[4]
);

void ConnectedSet(
    Pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int ClassLabel,
    unsigned int **seg,
    int *NumConPixels
);

int main(int argc, char **argv)
{
    FILE *fp;
    struct TIFF_img input_img;

    // if (argc != 2)
    //     error(argv[0]);

    // /* open image file */
    // if ((fp = fopen(argv[1], "rb")) == NULL)
    // {
    //     fprintf(stderr, "cannot open file %s\n", argv[1]);
    //     exit(1);
    // }
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
    double T = 1;
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
    save_grayscale_image_to_tiff_i(seg, input_img.width, input_img.height, "connected-set-1t.tif");
}

void ConnectedNeighbors(
    Pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int *M,
    Pixel c[4]
)
{
    unsigned char s_value = img[s.m][s.n];
    if (s.m != 0 && img[s.m-1][s.n] - s_value <= T) {
        Pixel p = {.m = s.m-1, .n = s.n};
        c[*M] = p;
        (*M)++;
    }
    if (s.n != 0 && img[s.m][s.n-1] - s_value <= T) {
        Pixel p = {.m = s.m, .n = s.n-1};
        c[*M] = p;
        (*M)++;
    }
    if (s.m != height-1 && img[s.m+1][s.n] - s_value <= T) {
        Pixel p = {.m = s.m+1, .n = s.n};
        c[*M] = p;
        (*M)++;
    }
    if (s.n != width && img[s.m][s.n+1] - s_value <= T) {
        Pixel p = {.m = s.m, .n = s.n+1};
        c[*M] = p;
        (*M)++;
    }
        
}

void ConnectedSet(
    Pixel s,
    double T,
    unsigned char **img,
    int width,
    int height,
    int ClassLabel,
    unsigned int **seg,
    int *NumConPixels
)
{
    Pixel startPoints[width*height];
    int index = 0;
    startPoints[index] = s;
    seg[s.m][s.n] = ClassLabel;
    while (index != -1) {
        s = startPoints[index--];
        int numNeighbors = 0;
        Pixel neighbors[4];
        // Find the neighbors of the pixel s
        ConnectedNeighbors(s, T, img, width, height, &numNeighbors, neighbors);
        for (int i = 0; i < numNeighbors; i++) {
            Pixel p = neighbors[i];
            // If we haven't marked this pixel as part of the set add it to the pixels to explore
            if (seg[p.m][p.n] == 0) {
                startPoints[++index] = p;
                // Mark this pixel as part of the connected set
                seg[s.m][s.n] = ClassLabel;
                // Increment the number of connected pixels
                (*NumConPixels)++;
            }
        }
    }
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
