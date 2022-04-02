# First thoughts

Havn't delve into nothing yet, I read the requirements and write whatever pops to mind.

## Functional Requirements

- Upload data to s3
- Upload metadata to a database
- Process uploaded data to s3 and create preprocessed data (Shouldn't it be postprocessed?)
- Ability to query metadata and receive data and postprocessed data as an environment on an ec2 machine

## Some estimations

- 10 sessions per day
- 600 MB per session

Meaning
- ~6GB data per day
- 20*6 = 120GB data per work month

Assuming network speed of 1Gbps
- It takes ~1 minute to upload 6GB

Conclusion - No issues in term of storage / network speed

## Initial bullets to remember

### Uploading data to the cloud

Specifically, data and metadata from disk to S3/Database.

__Security__ is a concern here

__Performance__ is something to think about, but is not critical according to the requirements of low scale, and the mentioned data size.

Both security and performance leads us to think about Vpn/Direct-Connect and/or Storage-Gateway.

### Processing as a post effect of uploading to S3

Triggers of course.

Need to think about lambda vs queue vs pubsub - It all comes down on latency requirements and type of workload.

I don't see a good reason (now) for pubsub.

If the latency is not critical, and the processing is not more than 15 minutes, lambda is a good candidate.

For other, more serious work we can utilize sqs. From what I can tell, we can use the Fifo mode because the rate at which changes apply is (very low). This way we won't have to deal with annoying issues such as receiving the same messages and have to implement the consumers in a homoegeneous way.

### S3 Policies and lifecycles

As indicated, removing data should be hard. We can, and should have proper roles in the system that provides different access permissions. Upload will upload only. No need for any systematic user to have delete permissions.

Also, We can enable versioning.

In addition, And I make an assumption here - Data that was collected X time ago is less interesting. Or even perhaps, data that has already been processed is less interesting. We can move it the Glaciar to reduce costs using predefined lifecycles (30 days or something like that).

### Metadata storage

I get the feeling that querying the metadata should be low latency in order to provide ad-hoc investigation in order to find the correct data to fetch.

Also, there is no specific (Useful) schema that can be utilized here.

The above leads me to believe we should not utilize a relational database rather than something like ElasticSearch.

### EC2 bringup with data in a staging environment

First of all, I can't recall exactly, but there is a way to embed the roles inside the node itself to have specific permissions. We can utilize this.

Second, we need to think about what we need to do with the data. EBS ofcourse is the fastest, but it is really volatile. Should we use EFS, FSx Lustre perhaps? For now, under the specified requirements, I don't think so.