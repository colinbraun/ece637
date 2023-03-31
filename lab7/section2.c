#include <math.h>
#include <tiff.h>
#include <allocate.h>
#include <randlib.h>
#include <typeutil.h>
#include "util.h"

void error(char *name);
int compare( const void* a, const void* b);

typedef struct pair
{
    // A pair of ints. When sorting pairs, sorts by m.
    int m, n;
} Pair;

int sum(Pair* arr, size_t length, int start, int end);

int main(int argc, char **argv)
{
    FILE *fp;
    struct TIFF_img original_img;
    struct TIFF_img img14gn_img;
    struct TIFF_img img14sp_img;

    char *fileName = "img14g.tif";
    if ((fp = fopen(fileName, "rb")) == NULL)
    {
        fprintf(stderr, "cannot open file %s\n", fileName);
        exit(1);
    }
    /* read image */
    if (read_TIFF(fp, &original_img))
    {
        fprintf(stderr, "error reading file %s\n", fileName);
        exit(1);
    }
    /* close image file */
    fclose(fp);
    /* check the type of image data */
    char imageType = 'g';
    if (original_img.TIFF_type != imageType)
    {
        fprintf(stderr, "error:  Wrong image type\n");
        exit(1);
    }
    read_TIFF(fopen("img14gn.tif", "rb"), &img14gn_img);
    read_TIFF(fopen("img14sp.tif", "rb"), &img14sp_img);

    unsigned int **result = (unsigned int **)get_img(original_img.width, original_img.height, sizeof(unsigned int));
    
    // Flip colors of images
    Pair weights[25];
    weights[0].n = 1; weights[1].n = 1; weights[2].n = 1; weights[3].n = 1; weights[4].n = 1; weights[5].n = 1; weights[6].n = 2;
    weights[7].n = 2; weights[8].n = 2; weights[9].n = 1; weights[10].n = 1; weights[11].n = 2; weights[12].n = 2; weights[13].n = 1;
    weights[14].n = 1; weights[15].n = 1; weights[16].n = 2; weights[17].n = 2; weights[18].n = 2; weights[19].n = 1; weights[20].n = 1;
    weights[21].n = 1; weights[21].n = 1; weights[22].n = 1; weights[23].n = 1; weights[24].n = 1;
    for (int row = 2; row < original_img.height-2; row++) {
        for (int col = 2; col < original_img.width-2; col++) {
            Pair window[25];
            for (int i = -2; i <= 2; i++) {
                for (int j = -2; j <= 2; j++) {
                    int index = (i+2)*(j+2) + j+2;
                    window[index].m = img14sp_img.mono[row+i][col+i];
                    window[index].n = weights[index].n;
                }
            }
            qsort(window, 25, sizeof(Pair), compare);
            int i = 0;
            while (sum(window, 25, 0, i) < sum(window, 25, i+1, 25)) {
                i++;
            }
            result[row][col] = window[i].m;
        }
    }
    save_grayscale_image_to_tiff_i(result, original_img.width, original_img.height, "2-img14sp-corrected.tif");
}

// Sum all the weights between start and end in the array.
int sum(Pair* arr, size_t length, int start, int end)
{
    int total = 0;
    for(int i = start; i < end; i++) {
        total += arr[i].n;
    }
    return total;
}

int compare(const void* a, const void* b)
{
    Pair pair_a = *((Pair *)a);
    Pair pair_b = *((Pair *)b);

    if (pair_a.m == pair_b.m)
        return 0;
    else if (pair_a.m < pair_b.m)
        return -1;
    else
        return 1;
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
