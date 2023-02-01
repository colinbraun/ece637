#include "allocate.h"
#include "tiff.h"

typedef struct pixel
{
    int m, n; /* m=row, n=col */
} Pixel;


double ***get_color_image(size_t width, size_t height);
void free_color_image(void ***pt);
void save_color_image_to_tiff(double ***img, size_t width, size_t height, char *filename);
void save_grayscale_image_to_tiff(double **img, size_t width, size_t height, char *filename);
// unsigned char type image of the above version of the above
void save_grayscale_image_to_tiff_c(unsigned char **img, size_t width, size_t height, char *filename);
// unsigned char type image of the above version of the above
void save_grayscale_image_to_tiff_i(unsigned int **img, size_t width, size_t height, char *filename);
double **convolve(double **img, size_t width, size_t height, double **h, size_t h_width, size_t h_height);
double ***tiff_to_double(struct TIFF_img *tiff_img);

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