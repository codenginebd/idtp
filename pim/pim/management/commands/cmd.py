import os
import json
from datetime import datetime
import xmltodict
from django.core.management.base import BaseCommand

from lib.iso_20022_extractor import ISO20022Extractor
from lib.ws_xml_parser import WSXMLParser


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Inside test command")
        r = "<GetFIUserListResponse>  <Code>200</Code>  <Message>Success</Message>  <UserInfo seqNum=\"1\">    <FullName>FARZANA AFROSE</FullName>    <VirtualID>farzanascbl@user.idtp</VirtualID>    <AddressLine1>HOUSE-121/122, AVENUE-03</AddressLine1>    <AddressLine2>ROAD- 01, MIRPUR DOHS</AddressLine2>    <ContactNo>01833181074</ContactNo>    <Email>moyi2o@gmail.com</Email>    <NID>19832692619564271</NID>    <TIN>787244324394</TIN>    <BIN />    <DateOfBirth>1984-08-31 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-10T12:30:36.1233333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02333556901</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"2\">    <FullName>MD. MAIDUL HOQUE</FullName>    <VirtualID>maidulscbl@user.idtp</VirtualID>    <AddressLine1>TECHNICAL ANALYST</AddressLine1>    <AddressLine2>STANDARD CHARTERED BANK</AddressLine2>    <ContactNo>01672219300</ContactNo>    <Email>pavel.ete@gmail.com</Email>    <NID>2692619471497</NID>    <TIN>275238466526</TIN>    <BIN />    <DateOfBirth>1987-11-26 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-10T12:28:46.1133333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02123254801</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"3\">    <FullName>MUHAMMAD ANWAR RASHID SHIDDKI</FullName>    <VirtualID>pavelscbl@user.idtp</VirtualID>    <AddressLine1>SR. TECHNICAL ANALYST</AddressLine1>    <AddressLine2>IT DEPARTMENT LEVEL 3 67 GULSHAN</AddressLine2>    <ContactNo>01713081822</ContactNo>    <Email>anwar-rashid.pavel@sc.com</Email>    <NID>2697556384113</NID>    <TIN>610028545172</TIN>    <BIN />    <DateOfBirth>1978-01-01 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-10T12:26:44.4033333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>18180936901</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"4\">    <FullName>MD SHARIFUL ISLAM</FullName>    <VirtualID>sharifulscbl@user.idtp</VirtualID>    <AddressLine1>MANAGER,BUSINESS SYSTEMS,SCB</AddressLine1>    <AddressLine2>ID-1550608, SCB HOUSE, 3RD FLOOR</AddressLine2>    <ContactNo>01623067403</ContactNo>    <Email>CODENGINEBD@GMAIL.COM</Email>    <NID>19881911872733322</NID>    <TIN>766823887641</TIN>    <BIN />    <DateOfBirth>1988-08-15 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-10T12:22:32.6633333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02109152801</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"5\">    <FullName>SABRINA SHARMIN TAMANNA</FullName>    <VirtualID>tamannascbl@user.idtp</VirtualID>    <AddressLine1>316, NORTH SHAJAHANPUR</AddressLine1>    <AddressLine2 />    <ContactNo>01817298042</ContactNo>    <Email>sabrinasharmin.tamanna@sc.com</Email>    <NID>2695434995065</NID>    <TIN>524352618917</TIN>    <BIN />    <DateOfBirth>2001-09-25 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-07T13:12:16.4433333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02109114401</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"6\">    <FullName>JAHANGIR MOHAMMED JAVED</FullName>    <VirtualID>javedscbl@user.idtp</VirtualID>    <AddressLine1>INFORMATION TECHNOLOGY DEPARTMENT</AddressLine1>    <AddressLine2>(LEVEL-3), 67 GULSHAN AVENUE</AddressLine2>    <ContactNo>01713081824</ContactNo>    <Email>mohammed-javed.jahangir@sc.com</Email>    <NID>2698879312781</NID>    <TIN>564663939002</TIN>    <BIN />    <DateOfBirth>1978-01-17 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-03T13:17:37.9833333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02348931001</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"7\">    <FullName>MD. KAMRUL AHSAN</FullName>    <VirtualID>kahsanscbl@user.idtp</VirtualID>    <AddressLine1>35/2, MUNSHI BARI ROAD</AddressLine1>    <AddressLine2>ZIGATOLA, DHANMONDI</AddressLine2>    <ContactNo>01713304901</ContactNo>    <Email>m-kamrul.ahsan@sc.com</Email>    <NID>8221137923</NID>    <TIN>772736874753</TIN>    <BIN />    <DateOfBirth>1964-01-01 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-02T18:27:00.2633333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02111376301</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"8\">    <FullName>MOHAMMED MOSTAFA KAMAL</FullName>    <VirtualID>sohelscbl@user.idtp</VirtualID>    <AddressLine1>STANDARD CHARTERED BANK, IT</AddressLine1>    <AddressLine2>3RD FLOOR, 67, GULSHAN AVENUE</AddressLine2>    <ContactNo>01678636246</ContactNo>    <Email>sohel327@yahoo.com</Email>    <NID>6855014681</NID>    <TIN>263772712514</TIN>    <BIN />    <DateOfBirth>1979-01-02 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-02T18:20:14.2833333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02348950701</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"9\">    <FullName>APURBA KRISHNA BALA</FullName>    <VirtualID>apurbascbl@user.idtp</VirtualID>    <AddressLine1>67, GULSHAN AVENUE, PARTLINK</AddressLine1>    <AddressLine2>TOWER</AddressLine2>    <ContactNo>01730068824</ContactNo>    <Email>APURBA.BALA@GMAIL.COM</Email>    <NID>3513282342210</NID>    <TIN>792277618091</TIN>    <BIN />    <DateOfBirth>1982-10-06 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-02T10:26:54.3966667</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02130987501</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"10\">    <FullName>02537654801</FullName>    <VirtualID>saidulscbl@user.idtp</VirtualID>    <AddressLine1>FLAT-5H, AMINA'S PEARL</AddressLine1>    <AddressLine2>62-63,BOROBAGH,MIRPUR-02</AddressLine2>    <ContactNo>01713082705</ContactNo>    <Email>shaon.scb@gmail.com</Email>    <NID>4156294524</NID>    <TIN>312398477714</TIN>    <BIN />    <DateOfBirth>1983-04-22 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-02T10:21:44.0033333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02537654801</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"11\">    <FullName>Md Shariful Islam</FullName>    <VirtualID>shariful3@user.idtp</VirtualID>    <AddressLine1>Uttara</AddressLine1>    <AddressLine2>Dhaka</AddressLine2>    <ContactNo>01623067413</ContactNo>    <Email>MdShariful.Islam@sc.com</Email>    <NID>1911872755539</NID>    <TIN>124536547816</TIN>    <BIN />    <DateOfBirth>1988-08-15 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-02-01T15:51:03.9733333</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02109152825</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"12\">    <FullName>James Bond</FullName>    <VirtualID>james.bond@user.idtp</VirtualID>    <AddressLine1>Sector 09</AddressLine1>    <AddressLine2>Dhaka</AddressLine2>    <ContactNo>01325556453</ContactNo>    <Email>james.bond@sc.com</Email>    <NID>1915872733322</NID>    <TIN>123456799215</TIN>    <BIN />    <DateOfBirth>1981-08-15 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-01-27T15:15:15.12</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>05215485603</AccountNumber>    </FIInfo>  </UserInfo>  <UserInfo seqNum=\"13\">    <FullName>Md Shariful Islam</FullName>    <VirtualID>shariful@user.idtp</VirtualID>    <AddressLine1>Sector 09</AddressLine1>    <AddressLine2>Uttara</AddressLine2>    <ContactNo>01623067403</ContactNo>    <Email>mdshariful.islam@sc.com</Email>    <NID>1911872733322</NID>    <TIN>123456789215</TIN>    <BIN />    <DateOfBirth>1988-08-15 00:00:00</DateOfBirth>    <DateOfIncorporation />    <CreatedOn>2021-01-25T12:33:41.9066667</CreatedOn>    <FIInfo seqNum=\"1\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>05215425603</AccountNumber>    </FIInfo>    <FIInfo seqNum=\"2\">      <FIName>Standard Chartered</FIName>      <FIBranch />      <RoutingNumber />      <AccountNumber>02109152821</AccountNumber>    </FIInfo>  </UserInfo></GetFIUserListResponse>"
        response_dict = WSXMLParser.parse_response(r)

