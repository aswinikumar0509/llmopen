import re

def extract_judgment_metadata(text):
    metadata = {}

    # 1. Court Name
    metadata['Court Name'] = "Supreme Court of India" if "SUPREME COURT OF INDIA" in text.upper() else "Not Found"

    # 2. Judgment Date and Year
    date_match = re.search(r'DATE OF JUDGMENT:\s*(\d{2}/\d{2}/\d{4})', text)
    if date_match:
        metadata['Judgment Date'] = date_match.group(1)
        metadata['Judgment Year'] = date_match.group(1).split('/')[-1]
    else:
        metadata['Judgment Date'] = metadata['Judgment Year'] = "Not Found"

    # 3. Case Name
    pet = re.search(r'PETITIONER:\s*(.*?)\s+Vs\.', text, re.DOTALL)
    resp = re.search(r'RESPONDENT:\s*(.*?)\n', text)
    if pet and resp:
        metadata['Case Name'] = f"{pet.group(1).strip()} vs {resp.group(1).strip()}"
    else:
        metadata['Case Name'] = "Not Found"

    # 4. Judge Names
    judges = re.findall(r'BENCH:\s*(.+?)\n', text)
    unique_judges = list(set(judge.strip() for judge in judges if judge.strip()))
    metadata['Judge Name(s)'] = ', '.join(unique_judges) if unique_judges else "Not Found"

    # 5. Case Type & Number (from mentions like Writ Petition No.)
    case_match = re.findall(r'(Writ|Civil|Criminal)[\s\S]*?(?:Petition|Appeal)[^\d]*(\d+/?\d+)', text, re.IGNORECASE)
    if case_match:
        metadata['Case Type and Number'] = [f"{c[0]} Petition No. {c[1]}" for c in case_match]
    else:
        metadata['Case Type and Number'] = []

    # 6. Referred Citations (like "JT 1996 (2) 470", "1996 SCALE (2)312")
    citations = re.findall(r'\b(?:JT|SCC|AIR|SCR|SCALE|LLJ)[^\n]+', text)
    metadata['Referred Citations'] = list(set(c.strip() for c in citations))

    return metadata


# Usage Example
# with open('16050.txt', 'r', encoding='utf-8') as file:
#     text = file.read()
text=(""" IN THE SUPREME COURT OF INDIA
CIVIL APPELLATE JURISDICTION
CIVIL APPEAL No.3159 OF 2004
COMMISSIONER OF CENTRAL EXCISE, 

Judges: RANJAN GOGOI, J., ........................J., ........................................................J., .............................J.

Judgment Date: Not found

Final Decision: Not found

PDF Link: http://192.168.1.26:8000/pdf_sc/01-05-2018_to_31-05-2018/4__Judgement_11-May-2018.pdf

================================================================================
ENTIRE JUDGMENT TEXT:
================================================================================

1
REPORTABLE
IN THE SUPREME COURT OF INDIA
CIVIL APPELLATE JURISDICTION
CIVIL APPEAL No.3159 OF 2004
COMMISSIONER OF CENTRAL EXCISE, 
INDORE
 …APPELLANT(S)
     VERSUS
M/S GRASIM INDUSTRIES LTD.
THROUGH ITS SECRETARY  
 
…RESPONDENT(S)
WITH
C.A.  Nos.3455/2004,  7272/2005,  2982-2985/2005,  2986/2005,
7143/2005,  2261/2006,  2246-2247/2008,  2934-2935/2008,  3528/2008,
4820/2008,  6695/2008,  2534/2009,  253/2010,  8541/2009,  445/2010,
1382/2010,  2003-2004/2010,  2430/2010,  2363/2010,  7174-7175/2010,
4696/2011, 6984/2011, 2705/2012
J U D G M E N T
RANJAN GOGOI, J.
1.
First, the facts:
The respondent – Assessees are manufacturers of dissolved and
compressed industrial gases, liquid chlorine and other allied products.
Cotton  yarn  and  Post  Mix  Concentrate  manufactured  by  two  other
individual assessees are also in issue.  These articles are supplied to the
customers in tonners, cylinders, carboys, paper cones and HDPE bags,
BIBs, pipeline and canisters, which may be more conveniently referred to

2
as  “containers”.   In  some  cases  the  containers  are  provided  by  the
Assessees to the customers on rent whereas in others the customers
bring their own containers.  For making available or for filling up the
containers  provided  by  the  customers  the  Assessees  charge  the
customers certain amounts under different heads viz. packing charges,
wear and tear charges, facility charges, service charges, delivery and
collection  charges,  rental  charges,  repair  and  testing  charges.  The
Assessees treat the said amounts as their income from ancillary or allied
ventures.  
2.
The issue arising is whether the aforesaid charges realised by the
Assessees are liable to be taken into account for determination of value
for the purpose of levy of duty in terms of Section 4 of the Central Excise
Act, 1944 (hereinafter referred to as “the Act”) as amended with effect
from 1st July, 2000. 
3.
Perceiving a conflict between the two decisions of this court in
Union of India and Ors. v. Bombay Tyre International Ltd. and Ors.
 
 1
and Commissioner of Central Excise, Pondicherry  v. Acer India Ltd.2,
a two judge Bench of this Court by order dated 30th July, 20093 referred
the following questions for an answer by a larger bench:
1 (1984) 1 SCC 467
2 (2004) 8 SCC 173
3 (2009) 14 SCC 596

3
“1. Whether Section 4 of the Central Excise Act, 1944
(as  substituted  with  effect  from  1-7-2000)  and  the
definition  of  “transaction  value”  in  clause  (d)  of  sub-
section (3) of Section 4 are subject to Section 3 of the
Act?
2. Whether Sections 3 and 4 of the Central Excise
Act, despite being interlinked, operate in different fields
and what is their real scope and ambit?
3. Whether the concept of “transaction value” makes
any material departure from the deemed normal price
concept of the erstwhile Section 4(1)(a) of the Act?”
4.
As the decisions in  Bombay Tyre International Ltd. (supra) and
Acer India Ltd.  (supra) were rendered by Benches of Three Hon’ble
Judges of this Court, the above questions were referred by order dated
30th March, 20164 to an even larger Bench.  This is how we are in seisin of
the matter.
5.
What is excise duty and what is the relationship between the nature
of the duty and the measure of the levy are the two precise questions that
would arise for determination in the present reference.   
6.
On first principles, there can be no dispute.   Excise is a levy on
manufacture and upon the manufacturer who is entitled under law to pass
on the burden to the first purchaser of the manufactured goods.  The levy
of excise flows from a constitutional authorisation under Entry 84 of List I
4 (2016) 6 SCC 391

4
of  the Seventh  Schedule  to  the  Constitution  of  India.   The  stage  of
collection of the levy and the measure thereof is, however, a statutory
function. So long the statutory exercise in this regard is a competent
exercise of legislative power, the legislative wisdom both with regard to
the stage of collection and the measure of the levy must be allowed to
prevail.   The measure of the levy must not be confused with the nature
thereof though there must be some nexus between the two.  But the
measure cannot be controlled by the rigors of the nature.  These are
some of the settled principles of laws emanating from a long line of
decisions of this Court which we will take note of shortly.  Do these
principles that have withstood the test of time require a rethink is the
question that poses for an answer in the present reference. 
7.
At this stage, it may be necessary to specifically take note of the
provisions of Sections 3 and 4 as originally enacted and as amended from
time to time.
Section 3
Section 3 of the Act in force
prior to amendment by Finance
Act 2000 (Act 10 of 2000)
Relevant portion of Section 3 as
substituted/amended (with effect
from 12th May, 2000) by Section
92  of  the  Finance  Act,  2000
(No.10 of 2000)
3. Duties specified in the First 3. Duties specified in [the First

5
Schedule to be levied. – 
(1)  There  shall  be  levied  and
collected in such manner as may
be prescribed,-
(a)  a  duty  of  excise  on  all
excisable  goods  which  are
produced  or  manufactured  in
India  as,  and  at  the  rates,  set
forth in the First Schedule to the
Central Excise Tariff Act, 1985; 
(b)………… 
Schedule  and  the  Second
Schedule] to the Central Excise
Tariff Act, 1985] to be levied.-
There shall be levied and collected
in  such  manner  as  may  be
prescribed,-
(a)   a duty of excise to be called
the  Central  Value  Added  Tax
(CENVAT) on all excisable goods
which
 
are
 
produced
 
or
manufactured in India as, and at
the  rates,  set  forth  in  the  First
Schedule  to  the  Central  Excise
Tariff Act, 1985 (5 of 1986);
(b)………….
Section 4 
Section 4 as originally
enacted
 (in  the
Central  Excise  and
Salt Act, 1944), 
Section 4 as amended
by  Amendment  Act
No.22 of 1973
Section
 
4
 
as
amended by Finance
Act, 2000 with effect
from 1.7.2000
Determination
 
of
value
 
for
 
the
purposes of duty –
Where under this Act
any
 
article
 
is
chargeable with duty
at  a  rate  dependent
on  the  value  of  the
article,  such  value
shall  be  deemed  to
be  the  wholesale
cash price  for  which
an article of the like
kind  and  quality  is
sold or is capable of
being sold for delivery
Valuation
 
of
excisable  goods  for
purposes of charging
of duty of excise.- (1)
Where under this Act,
the  duty  of  excise  is
chargeable  on  any
excisable  goods  with
reference  to  value,
such  value  shall,
subject  to  the  other
provisions  of  this
section, be deemed to
be-
 (a)  the  normal  price
Valuation
 
of
excisable goods for
purposes
 
of
charging of duty of
excise.  -  (1)  Where
under  this  Act,  the
duty  of  excise  is
chargeable  on  any
excisable goods with
reference  to  their
value, then, on each
removal of the goods,
such value shall -
(a)  in  a  case

6
at  the  place  of
manufacture  and  at
the  time  of  its
removal  therefrom,
without
 
any
abatement
 
of
deduction  whatever
except trade discount
and  the  amount  of
duty then payable.
thereof, that is to say,
the price at which such
goods  are  ordinarily
sold  by  the  assessee
to  a  buyer  in  the
course  of  wholesale
trade for delivery at the
time  and  place  of
removal,  where  the
buyer is not a related
person and the price is
the  sole  consideration
for the sale: 
Provided that-
(i)
 
where,
 
in
accordance  with  the
normal practice of the
wholesale  trade  in
such  goods,  such
goods are sold by the
assessee  at  different
prices  to  different
classes of buyers (not
being related persons)
each such price shall,
subject
 
to
 
the
existence of the other
circumstances
specified in clause (a),
be  deemed  to  be  the
normal  price  of  such
goods  in  relation  to
each  such  class  of
buyers;
(ii)  where  such  goods
are  sold  by  the
assessee in the course
of wholesale trade for
delivery at the time and
place of removal at a
where the goods
are  sold  by  the
assessee,
 
for
delivery  at  the
time and place of
the  removal,  the
assessee and the
buyer  of  goods
are  not  related
and  the  price  is
the
 
sole
consideration  for
the  sale,  be  the
transaction value;
(b)  in  any  other
case,  including
the  case  where
the goods are not
sold, be the value
determined
 
in
such  manner  as
may
 
be
prescribed.
 
(2)
 
The
provisions of this
section  shall  not
apply  in  respect
of  any  excisable
goods for which a
tariff  value  has
been fixed under
sub-section (2) of
section 3.
(3)
 
For  
the
purpose  of  this

7
price  fixed  under  any
law for the time being
in force or at a price,
being  the  maximum,
fixed  under  any  such
law,
 
then,
notwithstanding
anything  contained  in
clause  (iii)  of  this
proviso,  the  price  or
the maximum price, as
the  case  may  be,  so
fixed, shall, in relation
to  the  goods so  sold,
be  deemed  to  be  the
normal price thereof;
 
(iii)  where  the
assessee  so  arranges
that  the  goods  are
generally  not  sold  by
him  in  the  course  of
wholesale trade except
to or through a related
person,  the  normal
price of the goods sold
by the assessee to or
through  such  related
person
 
shall
 
be
deemed to be the price
at  which  they  are
ordinarily  sold  by  the
related  person  in  the
course  of  wholesale
trade  at  the  time  of
removal,  to  dealers
(not  being  related
persons)  or  where
such  goods  are  not
sold to such dealers, to
dealers  (being  related
persons) who sell such
section,- 
(a)  "assessee"
means
 
the
person  who  is
liable to pay the
duty  of  excise
under  this  Act
and  includes  his
agent;
(b) persons shall
be deemed to be
"related" if - 
(i)   they are inter-
connected 
undertakings;
(ii)   they are 
relatives;
(iii)  amongst  them
the  buyer  is  a
relative
 
and
distributor  of  the
assessee, or a sub-
distributor  of  such
distributor; or
(iv)   they  are  so
associated that they
have
 
interest,
directly or indirectly,
in  the  business  of
each
 
other.
 
 Explanation. -  In
this clause - 
(i)“inter-connected

8
goods in retail;
 (b) where the normal
price of such goods is
not  ascertainable  for
the  reason  that  such
goods are not sold or
for  any  other  reason,
the
 
nearest
ascertainable
equivalent
 
thereof
determined  in  such
manner  as  may  be
prescribed.
 (2) Where, in relation
to any excisable goods
the  price  thereof  for
delivery at the place of
removal  is  not  known
and the value thereof is
determined
 
with
reference  to  the  price
for delivery at a place
other than the place of
removal,  the  cost  of
transportation from the
place of removal to the
place of delivery shall
be excluded from such
price.
 (3) The provisions of
this  section  shall  not
apply in respect of any
excisable  goods  for
which a tariff value has
been fixed under sub-
section (2) of section 3.
 (4) For the purposes
of this section,-
undertakings” shall
have the meaning
assigned  to  it  in
clause  (g)  of
section  2  of  the
Monopolies  and
Restrictive  Trade
Practices
 
Act,
1969 (64 of 1969);
and
(ii)“relative”  shall
have the meaning
assigned  to  it  in
clause  (41)  of
section  2  of  the
Companies  Act,
1956 (1 of 1956);
(c)
 
“place
 
of
removal” means – 
(i)  a factory or any
other  place  or
premises
 
of
production
 
or
manufacture of the
excisable goods;
(ii) a warehouse or
any other place or
premises  wherein
the
 
excisable
goods  have  been
permitted  to  be
deposited  without
payment  of  duty,
from  where  such
goods
 
are
removed;

9
 (a) " assessee" means
the  person  who  is
liable to pay the duty of
excise  under  this  Act
and includes his agent;
 (b) " place of removal"
means-
 (i)  a  factory  or  any
other
 
place
 
or
premises of production
or  manufacture  of  the
excisable goods; or
 (ii)  a  warehouse  or
any  other  place  or
premises  wherein  the
excisable  goods  have
been  permitted  to  be
deposited
 
without
payment of duty, 
from where such goods
are removed;
 (c)  "related  person"
means a person who is
so associated with the
assessee  that  they
have  interest,  directly
or  indirectly,  in  the
business of each other
and includes a holding
company, a subsidiary
company,  a  relative
and a distributor of the
assessee,  and  any
sub- distributor of such
distributor. 
Explanation.-  In  this
clause"
 
holding
company","  subsidiary
company and" relative"
have
 
the
 
same
(d)   “transaction
value”  means  the
price actually paid
or payable for the
goods, when sold,
and  includes  in
addition  to  the
amount  charged
as  price,  any
amount  that  the
buyer  is  liable  to
pay  to,  or  on
behalf  of,  the
assessee,
 
by
reason  of,  or  in
connection
 
with
the  sale,  whether
payable at the time
of  the  sale  or  at
any  other  time,
including,  but  not
limited  to,  any
amount  charged
for,  or  to  make
provision
 
for,
advertising
 
or
publicity, marketing
and
 
selling
organization
expenses, storage,
outward  handling,
servicing,
warranty,
commission or any
other  matter;  but
does  not  include
the amount of duty
of excise, sales tax
and other taxes, if

10
meanings  as  in  the
Companies Act, 1956 ;
(1 of 1956 )
(d)  "value",  in  relation
to
 
any
 
excisable
goods,-
 (i)  where  the  goods
are  delivered  at  the
time  of  removal  in  a
packed
 
condition,
includes  the  cost  of
such  packing  except
the cost of the packing
which  is  of  a  durable
nature
 
and
 
is
returnable by the buyer
to the assessee.
Explanation.-  In  this
sub- clause,"  packing"
means  the  wrapper,
container, bobbin, pirn,
spool,  reel  or  warp
beam  or  any  other
thing  in  which  or  on
which  the  excisable
goods  are  wrapped,
contained or wound;
 (ii)  does  not  include
the amount of the duty
of excise, sales tax and
other  taxes,  if  any,
payable on such goods
and,  subject  to  such
rules as may be made,
the  trade  discount
(such  discount  not
being  refundable  on
any
 
account
whatsoever) allowed in
accordance  with  the
normal practice of the
any,  actually  paid
or actually payable
on such goods.

11
wholesale trade at the
time  of  removal  in
respect of such goods
sold  or  contracted  for
sale. 
(e)  “wholesale  trade”
means
 
sales
 
to
dealers,
 
industrial
consumers,
Government,
 
local
authorities  and  other
buyers,  who  or  which
purchase
 
their
requirements/otherwise
than in retail.
8.
It may be appropriate, at this stage, to make a brief narration of the
developments in the particular branch of fiscal jurisprudence which is in
issue in the present cases.   The Central Provinces and Berar Sales of
Motor Spirit and Lubricants Taxation Act, 1938, (Central Provinces
and Berar Act No.XIV of 1938) authorised the levy and collection from
every retail dealer, as defined by the Act, a tax on the retail sales of motor
spirits and lubricants at the rate of five per cent on the value of such
sales.  The levy was challenged and what arose for decision before the
Federal Court on a reference, made by the Governor General under
Section 213 of the Government of India Act, 1935 (often referred to as
“the Constitution Act”) is the question whether the said levy was a duty of
excise under Entry 45 of List-I in the Seventh Schedule to the Constitution

12
Act  or a tax on sale of goods under Entry 48 of List II of the said
Schedule.  While the eventual answer in the reference holding the levy to
be a tax on sale of goods and therefore within the competence of the
Provincial Legislature is of no consequence to the present issue, what
may require a specific notice is that Entry 45 which empowered the
Federal Legislature to make laws with respect to “duties of excise on
tobacco and other goods manufactured or produced in India; except…”
corresponds  to  Entry  84  of  List-I  of  the  Seventh  Schedule  to  the
Constitution of India.  
9.
Some extracts from the opinion rendered by Chief Justice Gwyer(all
the Judges on the Bench gave their own opinions while agreeing to the
eventual conclusion) would throw light on the nature of the levy of excise
and is therefore being recollected below:- 
“The federal legislative power extends to making laws
with  respect  to  duties  of  excise  on  goods
manufactured or produced in India. "Excise" is stated
in  the  Oxford  Dictionary  to  have  been  originally
accise", a word derived through the Dutch from the
late Latin accensare, to tax; the modern form, which
ousted accise" at an early date, being apparently due
to a mistaken derivation from the Latin excidere, to
cut out. It was at first a general word for a toll or tax,
but  since  the  17th  century  it  has acquired  in  the
United  Kingdom  a  particular,  though  not  always
precise, signification. The primary meaning of “excise
duty” or “duty of excise” has come to be that of a tax
on certain articles of luxury (such as spirits, beer or

13
tobacco)  produced  or  manufactured  in  the  United
Kingdom,  and  it  is  used  in  contradistinction  to
customs duties on articles imported into the country
from  elsewhere.  At  a  later  date  the  licence  fees
payable by persons who produced or sold excisable
articles also became known as duties of excise; and
the expression was still later extended to licence fees
imposed  for  revenue,  administrative,  or  regulative
purposes on persons engaged in a number of other
trades  or  callings.  Even  the  duty  payable  on
payments for admission to places of entertainment in
the United Kingdom is called a duty of excise; and,
generally speaking, the expression is used to cover
all duties and  taxes which,  together  with  customs
duties,  are  collected  and  administered  by  the
Commissioners  of  Customs  and  Excise.   But  its
primary and fundamental meaning in English is still
that of a tax on articles produced or manufactured in
the  taxing  country  and  intended  for  home
consumption.  I  am  satisfied  that  that  is  also  its
primary and fundamental meaning in India; and no
one has suggested that it has any other meaning in
Entry (45).
xxx
xxx
xxx
xxx
xxx
xxx
…There can be no reason in theory why an excise
duty should not be imposed even on the retail sale of
an  article,  if  the  taxing  Act  so  provides.  Subject
always to the legislative competence of the taxing
authority, a duty on home produced goods will
obviously  be  imposed  at  the  stage  which  the
authority find to be the most convenient and the
most lucrative, wherever it may be; but that is a
matter of the machinery of collection, and does
not  affect  the  essential  nature  of  the  tax. The
ultimate incidence of an excise duty, a typical indirect
tax, must always be on the consumer, who pays as
he consumes or expends; and it continues to be an
excise  duty,  that  is,  a  duty  on  home-produced  or
home-manufactured goods, no matter at what stage it
is  collected.  The  definition  of  excise  duties  is

14
therefore of little assistance in determining the extent
of the legislative power to impose them; for the duty
imposed by a restricted legislative power does not
differ  in  essence  from  the  duty  imposed  by  an
extended one.
It was argued on behalf of the Provincial
Government that an excise duty was a  tax on
production or manufacture only and that it could
not  therefore  be  levied  at  any  later  stage.
Whether or not there be any difference between a
tax  on  production  and  a  tax  on  the  thing
produced, this contention, no less than that of
the Government of India, confuses the nature of
the duty with the extent of the legislative power to
impose it.   Nor, for the reasons already given, is
it  possible  to  agree  that  in  no  circumstances
could  an  excise  duty  be  levied  at  a  stage
subsequent to production or manufacture.”
(Underlining and bold is ours)
10.
The issue was considered further in The Province of Madras
 
   vs.
Messrs. Boddu Paidanna & Sons
 
 5.     The following observation would
be relevant.
“In 1939 F.C.R. 18 the opinions expressed were
advisory opinions only, but we do not think that we
ought to regard them as any less binding upon us
on that account. We accept, therefore, the general
division  between  the  Central  and  Provincial
spheres of taxation which commended itself to the
majority of the Court in that case…………….. They
recognized that the expression 'duty of excise' is
wide enough to include a tax on sales ; but where
power is expressly given to another authority to
levy a tax on sales, it is clear that “duty of excise”
5 A.I.R. (29) 1942 Federal Court 33 (from Madras)

15
must be given a more restricted meaning than it
might otherwise bear. On the other hand the fact
that “duty of excise” is itself an expression of very
general import is no reason at all for refusing to
give to the expression “tax on sales” the meaning
which it would ordinarily and naturally convey. In
these circumstances the question at issue in the
present appeal appears to us to lie within a very
small compass.
The  duties of  excise  which  the  Constitution  Act
assigns exclusively to the Central Legislature are,-
according to the 1939 F.C.R 18, duties levied upon
the  manufacturer  or  producer  in  respect  of  the
manufacture or production of the commodity taxed.
The tax on the sale of goods, which the Act assigns
exclusively to the Provincial Legislatures, is a tax
levied on the occasion of the sale of the goods.
Plainly a tax levied on the first sale must in the
nature  of  things  be  a  tax  on  the  sale  by  the
manufacturer or producer ; but it is levied upon him
qua seller and not qua manufacturer or producer.
……………If the taxpayer who pays a sales tax is
also a manufacturer or producer of commodities
subject to a central duty of excise, there may no
doubt be an overlapping in one sense ; but there is
no overlapping in law. The two taxes which he is
called on to pay are economically two separate and
distinct imposts.  There is in theory nothing to
prevent the Central Legislature from imposing
a duty of excise on a commodity as soon as it
comes into existence, no matter what happens
to it afterwards, whether it be sold, consumed,
destroyed, or given away.  A taxing authority
will not ordinarily impose such a duty, because
it is much more convenient administratively to
collect the duty (as in the case of most of the
Excise Acts) when the commodity leaves the

16
factory for the first time, and also because the
duty is intended to be an indirect duty which
the manufacturer or producer is to pass on to
the ultimate consumer, which he could not do if
the  commodity  had,  for  example,  been
destroyed in the factory itself. It is the fact of
manufacture  which  attracts  the  duty,  even
though it may be collected later ; and we may
draw attention to the Sugar Excise Act in which
it is specially provided that the duty is payable
not only in respect of sugar which is issued
from the factory but also in respect of sugar
which is consumed within the factory.  In the
case of a sales tax, the liability to tax arises on
the  occasion  of  a  sale,  and  a  sale  has  no
necessary  connexion  with  manufacture  or
production.   The  manufacturer  or  producer
cannot of course sell his commodity unless he
has first manufactured or produced it; but he is
liable, if at all, to a sales tax because he sells
and not because he manufactures or produces;
and he would be free from liability if he chose
to give away everything which came from his
factory.”
11.
The early views on the nature of excise duty as a levy and the stage
of collection thereof would make it clear that though the impost is on the
manufacture of an article the point of collection of the same need not
necessarily coincide with the time of manufacture.  The stage of collection
can and usually is a matter of administrative convenience and such stage,
normally, is the stage of clearance of article when it, for the first time,
enters the trade for sale.  The above position was affirmed by the Privy

17
Council  in  Governor-General  in  Council v.  Province  of  Madras
 
 6
wherein it was, inter alia, held as follows:
“The term " duty of excise " is a somewhat flexible
one:  it  may,  no  doubt,  cover  a  tax  on  first  and,
perhaps, on other sales: it may in a proper context
have  an  even  wider  meaning.    An  exhaustive
discussion of this subject, from which their Lordships
have obtained valuable assistance, is to be found in
the judgment of the Federal Court in 1939 F. C. R.
18. Consistently with this decision, their Lordships
are of opinion that a duty of excise is primarily a duty
levied upon a manufacturer or producer in respect of
the commodity manufactured or produced. It is a tax
upon goods not upon sales or the proceeds of sale of
goods. Here again, their Lordships find themselves in
complete accord with the reasoning and conclusions
of the Federal Court in the Boddu Paidanna case.
The two taxes, the one levied upon a manufacturer in
respect of his goods, the other upon a vendor in
respect of his sales, may, as is there pointed out, in
one sense overlap. But in law there is no overlapping.
The taxes are separate and distinct imposts. If in fact
they  overlap,  that  may  be  because  the  taxing
authority,  imposing  a  duty  of  excise,  finds  it
convenient to impose that duty at the moment when
the exciseable article leaves the factory or workshop
for the first time on the occasion of its sale.  But that
method  of  collecting  the  tax  is  an  accident  of
administration; it is not of the essence of the duty of
excise, which is attracted by the manufacture itself.”
12.
The above views received the consideration of this Court in  R.C.
Jall Parsi 
 
 v.   Union of India and anr
 
 7 . wherein this Court held that while
excise duty is essentially a duty on manufacture which is passed on to the
6  [A.I.R. (32) 1945 Privy Council 98]
7 AIR 1962 SC 1281 

18
consumer, the stage of collection, subject to legislative competence of the
taxing authority, could be at any stage convenient so long the character of
the levy i.e. duty on manufacture is not altogether lost.  The further view
expressed was to the effect that “the method of collection does not affect
the essence of the duty, but only relates to the machinery of collection for
administrative convenience.”
13.
It  will  hardly  be  necessary  to  reiterate  the  long  lines  of
pronouncements that have consistently followed
the  above  view,
except to make a little detailed reference to Bombay Tyre International
Ltd. (supra), not only because the true ratio of the decision in the said
case has to be understood for the purpose of this reference so as to deal
with  the  perceived  conflict  with  Acer  India  Ltd.  (supra)  but  also  on
account of the fact that the subject in issue had received a full and
detailed consideration of this Court.
14.
In Bombay Tyre International Ltd. (supra) the issue, shortly put,
was whether determination of assessable value for the levy of excise duty
can be only on the manufacturing cost and the manufacturing profit.  It
was contended before this Court, by relying on the decision of this Court
in A.K. Roy and Another vs. Voltas Limited
 
 8, that having regard to the
8 (1973) 3 SCC 503

19
character  of  the  levy  the  measure  must  be  restricted  thereto.   The
contention was rejected by referring to a long line of precedents including
those referred to herein above to hold that “the levy of a tax is defined
by its nature, while the measure of the tax may be assessed by its
own standard.  It is true that the standard adopted as the measure of
the levy may indicate the nature of the tax but it does not necessarily
determine  it.”.   The  further  view  expressed  in  Bombay  Tyre
International Ltd. (supra) is that merely because excise is a levy on
manufactured goods the value of the excisable article for the purpose of
levy cannot be limited to only the manufacturing cost plus manufacturing
profit. This Court went on to hold that “a broader based standard of
reference  may  be  adopted  for  the  purpose  of  determining  the
measure of the levy.  Any standard which maintains a nexus with the
essential character of the levy can be regarded as a valid basis for
assessing the measure of the levy.” 
15.
A reading of Section 4 of the Act, as originally enacted; as amended
by 1973 Amendment; and as further amended by 2000 Amendment would
clearly show that the value of the article for the purposes of levy of ad
valorem duty was with reference to the price i.e. ‘normal price’ prior to the
2000 Amendment and thereafter with reference to the ‘transaction value’
which has been defined (already extracted) to mean “the price actually

20
paid or payable for the goods, when sold, and includes in addition to the
amount charged as price……”
16.
The measure for the purpose of the levy is, therefore, essentially the
price charged in respect of a transaction which must necessarily be at
arm’s length.  Inclusions and additions that enrich the value of the Article
till its clearance are permissible additions to the price that can be taken
into account to determine ‘value’ under the old Section 4 (prior to 2000) as
well as the ‘transaction value’ under the amended section effective from
1.7.2000. While such additions have been judicially held to be permissible
under the old Act in  Bombay Tyre International Ltd. (supra) the very
same heads have been statutorily engrafted by the amendment made in
2000. 
17.
The price charged for a manufactured article at the stage when the
article  enters  into  the  stream  of  trade  in  order  to  determine  the
value/transaction value for computation of the quantum of excise duty
payable does not come into conflict with the essential character or nature
of the levy.  The measure is the value and value is related to price.  The
price charged at the stage of clearance, in addition to manufacturing cost
and  manufacturing  profit,  can  include  certain  value  additions  and
inclusions which enrich the value of the product to make it suitable for

21
sale or to facilitate such sale.  At this stage, impost has nothing to do with
the sale.  The impost is on manufacture.  But it is the value upto the stage
of the first sale that is taken as the measure. Doing so does not introduce
any inconsistency between the nature and character of the levy and the
measure adopted.  
18.
The  above  aspect  had  been  considered  in  Bombay  Tyre
International Ltd. (supra) on a specific contention advanced on behalf of
the Assessees that the deductions under the following heads should be
made from the sale price in the following terms:
“48. We now proceed to the question whether any
post-manufacturing expenses are deductible from the
price when determining the “value” of the excisable
article. The old Section 4 provided by the Explanation
thereto that in determining the price of any article
under that section no abatement or deduction would
be allowed except in respect of trade discount and
the amount of duty payable at the time of the removal
of the article chargeable with duty from the factory or
other  premises  aforesaid.  The  new  Section  4
provides by sub-section (2) that where the price of
excisable goods for delivery at the place of removal is
not known and the value is determined with reference
to the price for delivery at a place other than the place
of removal, the cost of transportation from the place
of removal to the place of delivery has to be excluded
from such price. The new Section 4 also contains
sub-section  (4)(d)(ii)  which  declares  that  the
expression “value” in relation to any excisable goods,
does not include the amount of the duty of excise,
sales tax and other taxes, if any, payable on such
goods and, subject to such rules as may be made,

22
the  trade  discount  (such  discount  not  being
refundable on any account whatsoever) allowed in
accordance with the normal practice of the wholesale
trade at the time of removal in respect of such goods
sold  or  contracted  for  sale.  Now  these  are  clear
provisions expressly providing for deduction, from the
price, of  certain  items of  expenditure.  But  learned
counsel for the assessees contend that besides the
heads  so  specified  a  proper  construction  of  the
section  does  not  prohibit  the  deduction  of  other
categories of post-manufacturing expenses. It is also
urged  that  although  the  new  Section  4(4)(d)(i)
declares that in computing the “value” of an excisable
article,  the  cost  of  packing  shall  be  included,  the
provision should be construed as confined to primary
packing and as not extending to secondary packing.
The  heads under  which  the  claim  to  deduction  is
made are detailed below:
(1) Storage charges.
(2)  Freight  or  other  transport  charges,  whether
specific or equalised.
(3) Outward handling charges, whether specific or
equalised.
(4) Interest on inventories (stocks carried by the
manufacturer after clearance).
(5) Charges for other services after delivery to the
buyer.
(6) Insurance after the goods have left the factory
gate.
(7) Packing charges.
(8) Marketing and Selling Organisation expenses,
including advertisement and publicity expenses.
(Underlining is ours)
19.
The above issue was answered by saying -  
 “50.  We  shall  now  examine  the  claim.  It  is
apparent that for the purpose of determining the
“value”, broadly speaking both the old Section 4 (a)
and the new Section 4(1)(a) speak of the price for
sale in the course of wholesale trade of an article

23
for  delivery  at  the  time  and  place  of  removal,
namely,  the  factory  gate.  Where  the  price
contemplated under the old Section 4 (a) or under
the new Section 4(1)(a) is not ascertainable, the
price is determined under the old Section 4(b) or
the new Section 4(1)(b). Now, the price of an article
is related to its value (using this term in a general
sense), and into that value have poured several
components, including those which have enriched
its value and given to the article its marketability in
the  trade.  Therefore,  the  expenses  incurred  on
account  of  the  several  factors  which  have
contributed to its value upto the date of sale, which
apparently would be the date of delivery, are liable
to be included. Consequently, where the sale is
effected at the factory gate, expenses incurred by
the assessee upto the date of delivery on account
of  storage  charges,  outward  handling  charges,
interest  on  inventories  (stocks  carried  by  the
manufacturer  after  clearance),  charges  for  other
services after delivery to the buyer, namely after-
sales  service  and  marketing  and  selling
organisation  expenses  including  advertisement
expenses cannot be deducted. It will be noted that
advertisement  expenses,  marketing  and  selling
organisation  expenses  and  after-sales  service
promote the marketability of the article and enter
into its value in the trade. Where the sale in the
course  of  wholesale  trade  is  effected  by  the
assessee through its sales organisation at a place
or places outside the factory gate, the expenses
incurred by the assessee upto the date of delivery
under the aforesaid heads cannot, on the same
grounds, be deducted. But the assessee will be
entitled to a deduction on account of the cost of
transportation  of  the  excisable  article  from  the
factory gate to the place or places where it is sold.
The cost of transportation will include the cost of
insurance on the freight for transportation of the
goods from the factory gate to the place or places
of delivery.”
(Underlining is ours)

24
20.
We find no room whatsoever for any disagreement with the above
view taken by this court in Bombay Tyre International Ltd. (supra).  It is
a view consistent with what was held by the Federal Court and the Privy
Council  in  Central  Provinces  and  Berar  (supra),Boddu  Paidanna
(supra) and Province of Madras (supra) and the decisions that followed
thereafter  including  the  decision  in  Voltas  Limited (supra)  and  Atic
Industries Limited vs. H.H. Dewa, Asstt. Collector of Central Excise
and  ors
 
 9 the  true  purport  of  which  was  explained  in  Bombay  Tyre
International  Ltd. (supra). Both  the  above  opinions were clarified  to
mean that neither of them lay down any proposition to the effect that the
excise  duty  can  be  levied  only  on  the  manufacturing  cost  plus  the
manufacturing profit only. 
21.
At this stage, the amendment to Section 3 by substitution of the
words “a duty of excise on all excisable goods” by the words “a duty of
excise  to  be  called  the  Central  Value  Added  Tax  (CENVAT)  on  all
excisable goods” is conspicuous. The amendment of Section 3 to the Act
not only incorporates the essentials of a changed concept of charging of
tax on additions to the value of goods and services at each stage of
production but also engrafts in the statute what was judicially held to be
permissible additions to the manufacturing cost and manufacturing profit
9 (1975) 1 SCC 499

25
in Bombay Tyre International Ltd. (supra).  This fundamental change by
introduction  of  the  concept  underlying  value-added  taxation  in  the
provisions of Section 3 really find reflection in the definition of ‘transaction
value’ as defined by Section 4(3)(d) of the Act besides incorporating what
was explicitly held to be permissible in Bombay Tyre International Ltd.
(supra). Section 4(3)(d), thus, defines ‘transaction value’ by specifically
including all value additions made to the manufactured article prior to its
clearance, as permissible additions to be price charged for purpose of the
levy. 
22.
This would bring us to a consideration of the decision of this Court
in  Acer India Ltd (supra).  The details need not detain us.  Softwares
which were duty free items and could be transacted as softwares came to
be combined with the computer hardware which was a dutiable item for
purposes of clearance.  The Revenue sought to take into account the
value of  the  computer  software  for  the  purposes of  determination  of
‘transaction value’ with regard to the computer.  This Court negatived the
stand of the Revenue taking the view that when software as a separate
item was not dutiable its inclusion in the hard-disk of the computer cannot
alter the duty liability of the software so as to permit the addition of the
price/value of the software for the purpose of levy of duty. It is in the

26
above context that the decision of this Court in Acer India Ltd. (supra)
has to be understood. The observations made in paragraph 84 thereof to
the effect that ‘transaction value’ defined in Section 4(3)(d) of the Act
would be subject to the charging provisions contained in Section 3 of the
Act will have viewed in the context of a situation where an addition of the
value of a non-dutiable item was sought to be made to the value of a
dutiable item for the purpose of determination of the transaction value of
the composite item. This is the limited context in which the subservience
of Section 4(3)(d) to Section 3 of the Act was expressed and has to be
understood.  If so understood, we do not see how the views expressed in
paragraph 84 of Acer India Ltd. (supra) can be read to be in conflict with
the decision of Bombay Tyre International Ltd. (supra).
23.
Accordingly, we answer the reference by holding that the measure
of the levy contemplated in Section 4 of the Act will not be controlled by
the nature of the levy. So long a reasonable nexus is discernible between
the measure and the nature of the levy both Section 3 and 4 would
operate in their respective fields as indicated above. The view expressed
in Bombay Tyre International Ltd.(supra) is the correct exposition of the
law in this regard. Further, we hold that “transaction value” as defined in
Section 4(3)(d) brought into force by the Amendment Act, 2000, statutorily

27
engrafts the additions to the ‘normal price’ under the old Section 4 as held
to be permissible in  Bombay Tyre International Ltd. (supra) besides
giving effect to the changed description of the levy of excise introduced in
Section 3 of the Act by the Amendment of 2000. Infact, we are of the view
that  there  is  no  discernible  difference  in  the  statutory  concept  of
‘transaction value’ and the judicially evolved meaning of ‘normal price’.
24.
The  above  answers  would  comprehend  the  issues  specifically
arising in all the three questions that have been referred for our opinion. 
…........................J.
   
        (RANJAN GOGOI)
........................J.
   
        (N.V. RAMANA)
........................J.
   
        (R. BANUMATHI)
........................................................J.
   
  (MOHAN M. SHANTANAGOUDAR)
….............................J.
   
        (S. ABDUL NAZEER)
NEW DELHI
MAY 11, 2018.""")

metadata = extract_judgment_metadata(text)

# Display metadata
for key, value in metadata.items():
    if isinstance(value, list):
        print(f"{key}:")
        for item in value:
            print(f"  - {item}")
    else:
        print(f"{key}: {value}")
