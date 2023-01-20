#include "allocate.h"
#include "tiff.h"

double ***get_color_image(size_t width, size_t height);
void free_color_image(void ***pt);
void save_color_image_to_tiff(double ***img, size_t width, size_t height, char *filename);
double **convolve(double **img, size_t width, size_t height, double **h, size_t h_width, size_t h_height);
double ***tiff_to_double(struct TIFF_img *tiff_img);