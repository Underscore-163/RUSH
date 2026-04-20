import asyncio
import trustme
import datetime
import utils

asyncio.run(utils.full_setup())

rush_ca=trustme.CA(organization_name="RUSH")

cert=rush_ca.issue_cert("localhost",
                   not_before=datetime.datetime(day=datetime.datetime.now().day,month=datetime.datetime.now().month,year=datetime.datetime.now().year),
                   not_after=datetime.datetime(day=1,month=1,year=datetime.datetime.now().year+100))

cert.private_key_pem.write_to_path("config/key.pem")
cert.private_key_and_cert_chain_pem.write_to_path("config/cert.pem")
rush_ca.cert_pem.write_to_path("config/ca_cert.pem")

