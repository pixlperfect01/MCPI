from mctypes import Block
from mctypes import Location
def noisy_chunk(noise, chunk_x: int, chunk_z: int) -> list:
    chunk = [[[0] * 16 for _ in range(16)] for _ in range(256)]
    height_map = [[0] * 16 for _ in range(16)]

    x_offset = 16 * chunk_x
    z_offset = 16 * chunk_z

    for y in range(5):
        for x in range(16):
            for z in range(16):
                n = noise.noise3d(x, y, z)

                if y < 3:  # I do this to get more of a gradient between the different layers of bedrock
                    if n >= 0:
                        chunk[y + 1][z][x] = Block(Location(None, x, y, z))
                elif n > 0:
                    chunk[y + 1][z][x] = Block(Location(None, x, y, z))

    frequency = 20
    octaves = [3, 7, 12]
    height_factor = 72  # how high the surface is
    # redistrib = 0.035 * (256 / height_factor)
    redistrib = 0.05 * (256 / height_factor)

    octave_inverted_sum = sum([1 / o for o in octaves])

    for z in range(16):
        for x in range(16):
            nx = (x + x_offset) / 16 / frequency
            nz = (z + z_offset) / 16 / frequency

            # octaves
            e = sum([(noise.noise2d(o * nx, o * nz) / o) for o in octaves])
            e /= octave_inverted_sum

            # account for noise2d() range (-1 to 1)
            e += 1
            e /= 2

            # redistribution
            e **= redistrib

            # world is 256 blocks high but fuck it
            e *= height_factor

            # block coords can't be floats
            e = int(e)

            for y in range(e):
                if y < (height_factor - 14):  # draw grass or water depending on height
                    chunk[y + 9][z][x] = Block(Location(None, x, y, z))
                else:
                    chunk[y + 9][z][x] = Block(Location(None, x, y, z))

                for i in range(9):  # draw dirt
                    chunk[y + i][z][x] = Block(Location(None, x, y, z))

                chunk[y][z][x] = Block(Location(None, x, y, z))  # draw stone

    # generate the bedrock layers
    for y in range(5):
        for z in range(16):
            for x in range(16):
                if y == 0:
                    chunk[y][z][x] = Block(Location(None, x, y, z))
                else:
                    n = noise.noise3d(x + x_offset, y, z + z_offset)

                    # I do this to get more of a gradient between the different layers of bedrock
                    if y < 2 and n >= 0:
                        chunk[y][z][x] = Block(Location(None, x, y, z))
                    elif n > 0:
                        chunk[y][z][x] = Block(Location(None, x, y, z))

    return chunk
