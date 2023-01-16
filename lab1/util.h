#include "allocate.h"
#include "tiff.h"

double ***get_color_image(size_t width, size_t height);
void free_color_image(void ***pt);
void save_color_image_to_tiff(double ***img, size_t width, size_t height, char *filename);