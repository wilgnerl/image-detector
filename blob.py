import cv2

params = cv2.SimpleBlobDetector_Params()

params.filterByColor = False

params.filterByArea = True
params.minArea = 400
params.maxArea = 200_000

# Filter by Circularity
params.filterByCircularity = False
# params.minCircularity = 0.2
# params.maxCircularity = 200

# Filter by Convexity
params.filterByConvexity = False
# params.minConvexity = 0.87
# params.maxConvexity = 1

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.9
params.maxInertiaRatio = 1

detector = cv2.SimpleBlobDetector_create(params)
