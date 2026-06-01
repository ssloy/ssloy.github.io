#include <cmath>
#include "tgaimage.h"

constexpr TGAColor white = {255, 255, 255, 255};

void line(int ax, int ay, int bx, int by, TGAImage &framebuffer, TGAColor color) {
    for (int x=ax; x<=bx; x++) {
        float t = (x-ax) / static_cast<float>(bx-ax);
        int y = std::round( ay + (by-ay)*t );
        framebuffer.set(x, y, color);
    }
}

int main(int argc, char** argv) {
    constexpr int width  = 64;
    constexpr int height = 64;
    TGAImage framebuffer(width, height, TGAImage::RGB);

    int ax =  17, ay =  4;
    int bx = 43, by = 59;

    line(ax, ay, bx, by, framebuffer, white);

    framebuffer.write_tga_file("framebuffer.tga");
    return 0;
}

