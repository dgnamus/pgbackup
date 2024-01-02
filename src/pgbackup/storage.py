def local(infile, outfile):
    outfile.write(infile.read())
    outfile.close()
    infile.close()

def remote(client, infile, bucket, name):
    client.upload_fileobj(infile, bucket, name)
