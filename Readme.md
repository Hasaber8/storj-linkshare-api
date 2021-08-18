# The distribution process of PixelExpericence archives with Storj consists in two steps, synchronization to Storj, and request the LinkShare API.

# Synchronization
### Using the Rclone software, the synchronization is done in a faster and more straightforward way. With one code line it is possible to do the transfer process to the Storj cloud. The documentation use can be found at https://www.storj.io/integrations/sync-for-rclone-tech-preview

# Uplink API
### We used Storj’s API called uplink(https://github.com/storj/uplink), this API makes possible for our systems to contact the Storj network with the objective in acquiring the information of the cloud hosted archives.

### The uplink resource cannot be integrated in a simpler way in the PixelExperience system, there’s libraries in Java and C languages, however we use PHP and Python in our infrastructure.  Therefore, it was necessary to create a local wrapper that could use the LinkShare binary as base. It was built a Docker image that works as a bridge between the two services. 

### Small description about each fuction has been given in the main app.py, docker makes setting up the same setup for alternative usages very easy.