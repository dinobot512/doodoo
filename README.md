--- doodoo rougelike ---

todo:

optimize amount of chunks rendered
chunks are never marked as unmodified once modified bug
DONE big constant datatype





Rendering Steps

init renderer
    set bounds, tiles, world, zoom scales
    init empty surface cache
    init empty good surface cache

    get cache_key with cx and zoom
    if chunk surface at zoom level is in good_surfaces & the chunk has not been modified
        return the chunk surface from good_surfaces
    else
        render the chunk

    in order for good

