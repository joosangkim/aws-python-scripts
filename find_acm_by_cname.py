import boto3
CNAMES=[]
PROFILES=['default']
for p in PROFILES:
    print(f"*** start profile {p}")
    session = boto3.Session(profile_name=p)
    client = session.client('acm')
    response = client.list_certificates(
        MaxItems=123)

    arns = response['CertificateSummaryList']

    for arn in arns:
        arnInfo=client.describe_certificate(
            CertificateArn=arn['CertificateArn']
        )
        domains = arnInfo['Certificate']['DomainValidationOptions']
        for domain in domains:
            try:
                CNAMES.index(domain['ResourceRecord']['Name'])
                print(domain['ResourceRecord']['Name'])
            except ValueError:
                continue
