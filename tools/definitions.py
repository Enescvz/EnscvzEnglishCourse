"""Original concise English explanations, checked for one taught sense per card."""
from pathlib import Path
import json
D=Path(__file__).resolve().parents[1]
GENERAL='''
acknowledge|To accept or admit that something is true or exists.
acquire|To get a skill, possession, or knowledge over time.
advocate|To publicly support an idea or cause.
allocate|To assign money, time, or resources to a purpose.
ambiguous|Open to more than one possible interpretation.
anticipate|To expect something and prepare for it.
apparent|Easy to recognize or understand from the evidence.
appreciate|To recognize the value of something or feel grateful for it.
arbitrary|Based on a personal choice rather than a clear rule.
assert|To state something firmly as true.
assess|To examine and judge the quality or importance of something.
assumption|Something accepted as true without enough evidence.
attain|To achieve something after effort.
authentic|Real, original, or genuinely what it claims to be.
awareness|Knowledge that a situation or problem exists.
bias|An unfair preference that affects judgment.
breakthrough|An important discovery or advance.
capability|The ability or power to do something.
coherent|Logical, clear, and connected in a consistent way.
compelling|Strong enough to capture interest or persuade.
comprehensive|Including nearly all relevant parts or details.
concede|To admit a point after initially resisting it.
concrete|Specific and real rather than abstract or vague.
consequence|A result or effect of an action or event.
considerable|Large enough to be noticeable or important.
consistent|Remaining similar or following the same pattern.
constraint|A limit that restricts what is possible.
contemplate|To think carefully about a possible action.
conventional|Following generally accepted practices or ideas.
convey|To communicate an idea, feeling, or message.
credible|Believable because of convincing supporting evidence.
crucial|Extremely important to an outcome.
cumulative|Increasing through successive additions over time.
decisive|Having the power to settle an issue or result.
dedicate|To commit time, effort, or resources to something.
deduce|To reach a conclusion by reasoning from evidence.
deficient|Lacking an amount or quality that is needed.
deliberate|Done consciously and intentionally.
demonstrate|To show or prove something with evidence or examples.
deprive|To prevent someone from having something necessary or wanted.
derive|To originate from or be obtained from something else.
deteriorate|To become worse in condition or quality.
distinct|Clearly different and separate from something else.
diverse|Containing people or things of many different kinds.
dominant|More powerful, noticeable, or influential than others.
dramatic|Very large, sudden, or striking in effect.
elaborate|To provide additional details about an idea.
eliminate|To remove something completely.
emerge|To appear or become known gradually.
emphasize|To give special importance to a point.
encounter|To meet or experience something unexpectedly.
endure|To survive or tolerate a difficult situation.
enhance|To improve the quality or effectiveness of something.
ensure|To make certain that something happens.
entail|To necessarily involve or require something.
establish|To create something or show it to be true.
evaluate|To examine something to determine its value or quality.
evident|Clearly visible or easy to recognize.
exceed|To be greater than a particular amount or limit.
exclude|To leave someone or something out.
exhaustive|Covering a subject in complete or very great detail.
expand|To make something larger or more extensive.
explicit|Expressed clearly and without leaving room for doubt.
exploit|To take unfair advantage of people or opportunities.
facilitate|To make a task or process easier.
feasible|Possible and practical to accomplish.
fluctuate|To move up and down irregularly.
formulate|To develop an idea or plan carefully.
fundamental|Basic and essential to a system or idea.
furthermore|Used to add another supporting point.
genuine|Sincere, real, or not artificial.
grant|To officially give someone a right, request, or permission.
highlight|To draw attention to an important detail.
hypothesis|A suggested explanation that can be tested.
identical|Exactly the same in every relevant way.
illustrate|To explain or show something through an example.
implement|To put a decision, plan, or system into effect.
imply|To suggest an idea without stating it directly.
incentive|Something that motivates a person to act.
incorporate|To include something as part of a larger whole.
inevitable|Certain to happen or impossible to avoid.
infer|To form a conclusion from clues or evidence.
inherent|Existing as a permanent or natural part of something.
initiative|A new plan or action designed to solve a problem.
insight|A clear and deep understanding of a situation.
integrate|To combine parts into a working whole.
interpret|To decide or explain what something means.
intricate|Having many small and complicated details.
investigate|To examine the facts in order to discover the truth.
justify|To show that an action or opinion has good reasons.
legitimate|Reasonable, lawful, or justified in a context.
maintain|To keep something at the same level or condition.
manipulate|To influence or control someone unfairly or skillfully.
marginal|Very small in amount or importance.
mitigate|To make a harmful effect less serious.
moderate|Neither very large nor very small in degree.
neglect|To fail to give needed care or attention.
notion|An idea or belief about something.
obscure|Not well known, easy to see, or easy to understand.
obtain|To get something through effort or a process.
ongoing|Continuing to happen or develop.
outcome|The result of an event, decision, or process.
overlook|To fail to notice something important.
overwhelmed|Feeling unable to cope with too many demands.
paradox|A situation that seems contradictory but may be true.
perceive|To notice or understand something in a particular way.
persist|To continue despite difficulties or over time.
perspective|A particular way of considering a situation.
plausible|Reasonable and possible, though not necessarily proven.
precise|Exact, detailed, and clearly defined.
predominant|The most common or influential in a group.
preliminary|Done or decided before a final stage.
presume|To suppose something is true without certain proof.
prioritize|To decide which things matter most and do them first.
profound|Deep, powerful, or far-reaching in effect.
prominent|Widely known, important, or easily noticeable.
prospect|A possibility that may happen in the future.
pursue|To work toward an aim or continue an activity.
rationale|The underlying reasons for a decision or action.
reinforce|To make an idea, structure, or skill stronger.
reluctant|Not willing or eager to do something.
remarkable|Unusual or impressive enough to deserve attention.
resilient|Able to recover from difficulty or pressure.
resolve|To solve a problem or disagreement.
retain|To keep something, including knowledge, over time.
reveal|To make something previously hidden known.
rigorous|Very careful, thorough, and strict in method.
scarce|Available only in small or insufficient amounts.
scenario|A possible sequence of events or situation.
scope|The range of things that something covers.
scrutinize|To examine something very carefully.
significant|Important or large enough to matter.
simultaneously|Happening at the same time.
skeptical|Doubting a claim until there is good evidence.
speculate|To make guesses without enough definite evidence.
stability|A state of being steady and not changing suddenly.
substantial|Large or important in amount or effect.
subtle|Not obvious; delicate or difficult to notice.
sustain|To keep something continuing over time.
tangible|Physical or clearly real and measurable.
tentative|Not final, definite, or fully agreed.
thorough|Careful and complete, leaving little unexamined.
threshold|A point or level that triggers a change.
transmit|To send information or a signal from one place to another.
trigger|To cause a process or reaction to begin.
ultimately|In the end, after other things have happened.
unprecedented|Never previously known or experienced.
undergo|To experience a process or change.
underlying|Fundamental but not immediately obvious.
undertake|To agree to take responsibility for a task.
valid|Reasonable, well-founded, or officially acceptable.
viable|Capable of working or succeeding in practice.
vulnerable|Exposed to harm or easily affected by danger.
widespread|Existing or happening over a large area or group.
affluent|Having a great deal of money or wealth.
alleviate|To reduce pain, trouble, or an unpleasant effect.
anecdote|A short account of an interesting real incident.
apt|Likely or inclined to behave in a certain way.
articulate|To express thoughts clearly in speech or writing.
bolster|To strengthen or support something.
cautious|Careful to avoid unnecessary risk.
compromise|To reach agreement by accepting some differences.
consecutive|Following one another without a break.
contradict|To state the opposite of another statement.
correlate|To have a statistical or observable relationship.
counterpart|A person or thing with a similar role elsewhere.
culminate|To reach a final or most important point.
discrepancy|A difference between things expected to match.
dispute|To disagree with or challenge a claim.
disrupt|To interrupt normal progress or activity.
distinguish|To recognize the difference between two things.
diminish|To become smaller or less important.
dilemma|A difficult choice between alternatives.
empathy|The ability to understand another person's feelings.
equivalent|Equal in value, amount, or effect.
ethical|Concerned with what is morally right or wrong.
exaggerate|To describe something as greater than it is.
exemplify|To be a clear example of something.
foster|To encourage or support the development of something.
grievance|A formal complaint about unfair treatment.
hostile|Unfriendly or openly opposed to someone.
impartial|Fair and not favoring either side.
inadequate|Not sufficient for a particular need.
inclined|Likely or disposed to think or act a certain way.
indispensable|So useful or necessary that it cannot be replaced.
intact|Complete and not damaged or altered.
intriguing|Interesting because it is unusual or mysterious.
irrelevant|Not connected to the issue being discussed.
leverage|To use a resource to gain the best possible advantage.
mandatory|Required by a rule or law.
mutual|Shared or experienced by two or more parties.
nuance|A small but important difference in meaning or tone.
objective|Not influenced by personal feelings or preferences.
obstacle|Something that blocks progress toward a goal.
outweigh|To be more important or valuable than something else.
persistent|Continuing firmly despite difficulty or opposition.
prevalent|Commonly found in a particular place or time.
reconcile|To make different ideas or accounts consistent.
redundant|Unnecessary because the same function is already served.
relevant|Directly connected to the matter being discussed.
repercussion|An unintended or often negative consequence.
skepticism|An attitude of questioning claims and seeking evidence.
sophisticated|Complex, advanced, or carefully designed.
spontaneous|Happening naturally without planning.
streamline|To simplify a process so it works more efficiently.
susceptible|Likely to be affected or harmed by something.
transparent|Open and clear about actions or decisions.
unanimous|Agreed upon by everyone involved.
undermine|To gradually weaken an idea, system, or trust.
versatile|Able to perform many different roles or functions.
warrant|To justify or make a particular action necessary.
whereas|Used to contrast two different facts or situations.
withdraw|To take back an offer or remove oneself from an activity.
withstand|To survive or resist pressure or damage.
'''
FINANCE='''
accounts payable|Amounts a company owes to suppliers for credit purchases.
accounts receivable|Amounts customers owe a company for delivered goods or services.
accrual accounting|Recording revenue and expenses when earned or incurred, not when cash changes hands.
cash accounting|Recording transactions when cash is received or paid.
accrued expense|An expense incurred but not yet paid or recorded in cash.
accrued revenue|Revenue earned but not yet billed or collected.
accrued interest|Interest that has accumulated but not yet been paid.
adjusting entry|An entry made at period-end to update account balances.
amortization|Allocation of an asset's cost or repayment of a loan over time, depending on context.
asset impairment|A decrease in an asset's recoverable value requiring recognition of a loss.
allowance for doubtful accounts|An estimate of receivables that may never be collected.
accounts aging|Grouping receivables by how long they have remained unpaid.
accounting period|The span of time covered by financial records or reports.
accounting policy|A set of principles an organization uses to prepare financial statements.
audit trail|A record that lets reviewers trace a transaction from source to report.
auditor's opinion|An independent auditor's conclusion about the financial statements.
balance sheet|A statement of assets, liabilities, and equity at a specific date.
bank reconciliation|Matching a company's cash records to its bank statement.
book value|An asset's or company's value as reported in its accounting records.
capital expenditure|Spending to acquire or improve long-term assets.
cash equivalents|Highly liquid short-term investments close to cash.
cash flow statement|A statement of operating, investing, and financing cash movements.
chart of accounts|A structured list of account names and codes used in accounting.
closing entry|An entry that transfers temporary-account balances at period-end.
contra asset|An account that reduces the carrying amount of a related asset.
cost allocation|Assigning shared costs to activities, departments, or products.
cost of goods sold|Direct cost of inventory sold during a period.
credit memo|A document reducing an invoice amount or amount owed.
current asset|An asset expected to become cash or be used within the operating cycle.
current liability|An obligation normally due within one year or operating cycle.
debit balance|An account balance where debits exceed credits.
deferred expense|A cost recognized as an asset before it becomes an expense.
deferred revenue|Cash received before the related goods or services are delivered.
depletion|Allocation of the cost of a natural resource as it is extracted.
depreciation|Allocation of the cost of a tangible asset over its useful life.
direct cost|A cost traceable to a specific product, service, or activity.
double-entry bookkeeping|A recording method in which every transaction affects at least two accounts.
earnings before interest and taxes|Profit measured before interest expense and income taxes.
expense recognition|Recording costs in the accounting periods to which they relate.
fair value|The price at which an asset or liability could be exchanged in an orderly market transaction.
fiscal year|A twelve-month financial reporting period, not necessarily a calendar year.
fixed asset|A long-lived tangible asset used in operations.
general ledger|The master record containing an organization's financial accounts.
goodwill|An intangible asset arising when a business is acquired for more than its identifiable net assets.
gross margin|Gross profit expressed as a percentage of revenue.
gross profit|Sales revenue minus the cost of goods sold.
historical cost|The original amount paid to acquire an asset.
income statement|A statement showing revenues, expenses, and profit or loss for a period.
indirect cost|A shared cost not directly traceable to a single product or activity.
intangible asset|An identifiable nonphysical resource with economic value.
inventory turnover|A measure of how often inventory is sold and replaced.
journal entry|A dated record of debits and credits for a transaction.
liability|A present obligation expected to require a transfer of economic resources.
long-term liability|An obligation not expected to be settled within the coming year or operating cycle.
management accounting|Financial analysis prepared to support internal business decisions.
matching principle|The concept of reporting related expenses in the period of the revenues they help generate.
materiality|The importance of information in influencing financial decisions.
net income|Profit remaining after all recognized expenses and taxes.
net loss|A negative result when expenses exceed revenues.
noncurrent asset|An asset expected to provide benefits beyond the short term.
operating expense|A cost incurred while running a business's ordinary activities.
operating income|Profit from core operations before financing and some other items.
outstanding invoice|A bill issued to a customer that has not yet been paid.
payroll expense|The cost of employee wages, salaries, and related compensation.
prepaid expense|An advance payment for future benefits recorded initially as an asset.
provision|A recognized liability involving uncertainty about its timing or amount.
purchase order|A buyer's formal document authorizing a purchase.
reconciliation|Comparing records to identify and resolve differences.
retained earnings|Accumulated profits kept in the business rather than distributed.
revenue recognition|The process of recording revenue when it is earned under applicable rules.
sales return|Goods returned by customers that reduce recorded sales.
shareholders' equity|The owners' residual interest after liabilities are deducted from assets.
straight-line depreciation|A method allocating equal depreciation expense across an asset's useful life.
subsidiary ledger|Detailed records supporting a control account in the general ledger.
tangible asset|A physical resource used or held by an organization.
tax liability|An amount of tax currently owed or expected to be paid.
trial balance|A report listing account balances to check that total debits equal total credits.
unearned revenue|Cash collected in advance for goods or services still owed.
variable cost|A cost that changes with output or activity level.
variance analysis|Comparing actual results to budgets or standards to explain differences.
working capital|Current assets minus current liabilities.
write-down|A reduction in the carrying amount of an asset.
write-off|Removal of an asset or receivable from the books, often due to loss or uncollectibility.
withholding tax|Tax taken from a payment and remitted by the payer.
break-even point|The volume at which total revenue equals total costs.
contribution margin|Revenue less variable costs, available to cover fixed costs and profit.
cost center|An organizational unit whose costs are tracked separately.
profit center|An organizational unit accountable for revenues and expenses.
budget variance|The difference between actual and planned financial figures.
operating budget|A plan for expected revenue and routine operating costs.
capital budgeting|Evaluating investments in long-term projects or assets.
absorption costing|A costing method assigning direct and manufacturing overhead costs to products.
activity-based costing|Assigning overhead using activities that drive costs.
standard costing|Using predetermined expected costs to assess production performance.
period cost|A cost expensed in the period rather than included in inventory.
product cost|A cost assigned to products, often including materials, labor, and overhead.
sunk cost|Money already spent that cannot be recovered.
opportunity cost|The benefit given up when choosing one alternative over another.
contingent liability|A possible obligation dependent on a future uncertain event.
subsequent event|An event occurring after the reporting date but before financial statements are issued.
internal control|Policies and procedures designed to reduce financial and operational risks.
segregation of duties|Dividing responsibilities to reduce error and fraud risk.
material misstatement|An error or omission large enough to influence decisions based on financial statements.
asset turnover|A measure of revenue generated relative to the asset base.
quick ratio|A liquidity measure using highly liquid current assets relative to current liabilities.
current ratio|Current assets divided by current liabilities.
receivables turnover|A measure of how frequently customers pay credit balances.
days sales outstanding|Average days a company takes to collect receivables.
inventory write-down|Reducing recorded inventory value when its value has fallen.
impairment loss|A recognized loss from a decline in an asset's carrying value.
lease liability|The present value of lease payments an organization owes.
right-of-use asset|A lessee's recognized right to use an asset during a lease term.
finance lease|A lease transferring substantially the risks and rewards of ownership.
operating lease|A lease not classified as a finance lease under the applicable rules.
consolidated statements|Financial statements presenting a parent and its subsidiaries as one group.
noncontrolling interest|The portion of subsidiary equity not owned by the parent.
intercompany transaction|A transaction between entities in the same corporate group.
foreign exchange gain|Profit created by a favorable change in currency values.
foreign exchange loss|Loss resulting from an unfavorable change in currency values.
stock-based compensation|Payment to employees or others using shares or share-based awards.
financial instrument|A contract creating a financial asset for one party and a liability or equity for another.
hedge accounting|Accounting treatment designed to reflect certain qualifying risk-hedging relationships.
cash-generating unit|The smallest asset group generating largely independent cash inflows.
segment reporting|Reporting selected financial results for distinct parts of a business.
related-party transaction|A deal between parties with an established close relationship.
financial disclosure|Information provided to explain a company's finances and risks.
restatement|Revision of previously issued financial statements to correct errors.
closing balance|An account's balance at the end of a period.
opening balance|An account's balance at the beginning of a period.
cost basis|An asset's value used for calculating gains or tax outcomes.
liquidity|The ease with which an asset can be converted to cash without a large loss.
solvency|A person's or firm's capacity to meet long-term obligations.
leverage ratio|A comparison indicating the extent of financing with borrowed funds.
debt-to-equity ratio|Total debt divided by owners' equity.
interest coverage ratio|Earnings relative to interest payments owed.
capital structure|The blend of debt and equity a firm uses to finance operations.
equity financing|Raising funds by selling ownership stakes.
debt financing|Raising funds by borrowing with an obligation to repay.
bond yield|The return an investor receives from holding a bond.
coupon rate|Annual bond interest as a percentage of face value.
face value|The nominal principal value stated on a security.
maturity date|The date when a loan or bond principal is due.
yield to maturity|A bond's annualized return if held to maturity under stated assumptions.
credit spread|The extra yield on a risky bond over a benchmark bond.
credit rating|An assessment of the likelihood a borrower will repay debts.
creditworthiness|How likely a person or company is to repay obligations.
default risk|The possibility a borrower fails to meet payment obligations.
counterparty risk|The risk that the other side of a deal fails to perform.
market risk|Potential loss resulting from changes in market prices.
operational risk|Risk from failed processes, people, systems, or external events.
systemic risk|The possibility that failure in one area destabilizes the wider financial system.
risk appetite|The amount and type of risk an organization is willing to take.
risk tolerance|The level of variation or loss an investor can withstand.
risk-adjusted return|Investment return evaluated in relation to the risk taken.
volatility|The extent to which an asset's returns change over time.
standard deviation|A statistic describing how spread out observations are.
correlation coefficient|A statistic measuring the strength and direction of a linear relationship.
portfolio diversification|Spreading investments across assets to reduce concentration risk.
asset allocation|Dividing investments among asset classes.
rebalancing|Changing portfolio weights to restore a target allocation.
benchmark index|An index used to compare investment performance.
index fund|A fund designed to track a specified market index.
exchange-traded fund|An investment fund whose shares trade on an exchange.
mutual fund|A pooled investment vehicle managed for multiple shareholders.
expense ratio|A fund's yearly operating costs as a percentage of its assets.
net asset value|Fund assets minus liabilities, often divided by outstanding shares.
market capitalization|Share price multiplied by the number of outstanding shares.
price-to-earnings ratio|Stock price divided by earnings per share.
price-to-book ratio|Market price relative to accounting book value per share.
earnings per share|Net earnings attributable to each outstanding common share.
dividend payout ratio|Dividends relative to earnings over a period.
dividend yield|Annual dividends divided by the current share price.
free cash flow|Cash generated after spending needed for long-term assets.
discounted cash flow|A valuation approach that converts expected future cash flows into present value.
net present value|The value of discounted future cash flows minus the initial investment.
internal rate of return|The discount rate making a project's net present value equal zero.
weighted average cost of capital|The blended required return on a firm's debt and equity financing.
cost of equity|Return required by shareholders for investing in a firm.
cost of debt|The effective interest cost a company pays on borrowing.
terminal value|Estimated value of a business beyond an explicit forecast period.
discount rate|The rate used to translate future cash flows into present value.
perpetuity|A stream of payments expected to continue indefinitely.
annuity|A series of equal payments made at regular intervals.
compounding|Earning returns on both the original amount and past returns.
compound interest|Interest calculated on principal plus previously earned interest.
simple interest|Interest calculated on the original principal only.
principal|The original amount borrowed or invested, excluding interest.
collateral|An asset pledged as security for a loan.
margin call|A request to deposit funds or securities to meet margin requirements.
short selling|Selling borrowed securities in expectation of buying them back later.
long position|Ownership or exposure that benefits when an asset rises in price.
short position|Exposure that generally benefits when an asset falls in price.
stop-loss order|An order intended to limit losses by triggering after a price level is reached.
limit order|An instruction to buy or sell at a specified price or better.
market order|An instruction to trade at the best available market price.
bid-ask spread|The difference between the highest buyer price and lowest seller price.
order book|A list of active buy and sell orders for an asset.
liquidity provider|A participant offering readily available buying or selling interest.
market maker|A participant quoting buying and selling prices to support trading.
arbitrage|Seeking profit from price differences for equivalent assets.
hedging|Taking a position intended to offset an existing risk.
derivative|A contract whose value depends on an underlying asset or index.
futures contract|A standardized agreement to buy or sell at a future date under set terms.
forward contract|A privately negotiated contract for a transaction at a future date.
option premium|The price paid to buy an option contract.
strike price|The price at which an option holder may buy or sell the underlying asset.
call option|A contract granting the right, not obligation, to buy at a stated price.
put option|A contract granting the right, not obligation, to sell at a stated price.
intrinsic value|An option's immediate exercise value, if positive.
time value of an option|The portion of an option price beyond its intrinsic value.
implied volatility|Expected volatility inferred from market option prices.
beta coefficient|A measure of a security's sensitivity to broader market movements.
alpha|Return above a specified risk-adjusted benchmark or expected return model.
sharpe ratio|Excess return over a risk-free rate divided by return volatility.
maximum drawdown|The largest peak-to-trough portfolio decline over a period.
capital gain|Profit from selling an asset for more than its cost basis.
realized gain|Profit recognized after a position is actually sold or settled.
unrealized gain|An increase in value of an asset that has not yet been sold.
inflation rate|The pace of increase in the general price level.
real interest rate|An interest rate adjusted for inflation.
nominal interest rate|The stated rate before adjusting for inflation.
yield curve|A chart of interest rates for bonds with different maturities.
inverted yield curve|A yield curve with shorter-term rates above longer-term rates.
monetary policy|Central bank actions influencing money, credit, and interest rates.
fiscal policy|Government spending and taxation decisions affecting the economy.
quantitative easing|Central-bank purchases of assets intended to ease financial conditions.
central bank reserves|Balances commercial banks or monetary authorities hold at the central bank.
foreign exchange rate|The price of one currency expressed in another currency.
currency depreciation|A decline in a currency's value relative to others.
currency appreciation|An increase in a currency's value relative to others.
balance of payments|A record of economic transactions between a country and the rest of the world.
current account deficit|A negative balance of current international payments and receipts.
sovereign debt|Debt borrowed by a national government.
investment-grade bond|A bond assigned a relatively strong credit rating.
high-yield bond|A bond with a lower credit rating and usually higher promised yield.
junk bond|An informal name for a below-investment-grade bond.
securitization|Pooling financial assets and issuing securities backed by their cash flows.
asset-backed security|A security supported by cash flows from a pool of financial assets.
mortgage-backed security|A security supported by payments from pooled mortgages.
initial public offering|The first public sale of a company's shares.
secondary offering|A sale of additional shares after an initial public offering.
underwriting|Assuming responsibility for placing securities or insuring a defined risk.
venture capital|Risk capital invested in young, high-growth companies.
private equity|Investment in privately held businesses or buyouts.
seed funding|Early funding used to develop a new business concept.
capital raise|A transaction designed to obtain new financing.
valuation multiple|A ratio comparing business value to earnings, revenue, or another metric.
enterprise value|The value of an entire business, often equity plus debt minus cash.
mergers and acquisitions|Transactions combining or transferring control of businesses.
due diligence|Detailed investigation of a business before a transaction.
goodwill impairment|A write-down when the value assigned to acquired goodwill cannot be supported.
liquidation|Selling assets and settling liabilities when winding down a business.
bankruptcy|A legal process dealing with an individual or firm's inability to pay debt.
restructuring|Changing a firm's debts, operations, or organization to improve viability.
covenant|A contractual condition a borrower or other party must meet.
debt service|Cash required to pay interest and principal due on debt.
refinancing|Replacing an existing loan or debt with a new financing arrangement.
loan-to-value ratio|The amount lent relative to the value of pledged property.
amortization schedule|A table showing scheduled payments of principal and interest.
balloon payment|A large final payment due at the end of a loan.
prepayment penalty|A fee charged for repaying a debt before the agreed date.
escrow account|An account where a neutral party temporarily holds money or assets.
fiduciary duty|A legal obligation to act in another party's best interest.
compliance risk|Risk of loss or penalties from breaking laws, regulations, or standards.
financial statement analysis|Reviewing financial reports to assess performance and position.
sensitivity analysis|Testing how changes in one assumption affect an outcome.
scenario analysis|Studying different possible combinations of future conditions.
stress testing|Evaluating financial resilience under severe hypothetical conditions.
forecast accuracy|How closely predictions match actual results.
cash burn rate|How quickly a company consumes available cash.
cash runway|Estimated time until a company runs out of cash at its current burn rate.
customer acquisition cost|Average cost to gain one new customer.
lifetime value|Estimated net value a customer brings throughout the relationship.
unit economics|Revenues and costs associated with a single unit, customer, or transaction.
revenue growth|The increase in income from sales or services between periods.
profit margin|Profit measured as a share of revenue.
return on equity|Profit attributable to shareholders relative to equity.
return on assets|Net profit relative to the assets used to produce it.
return on investment|Gain or loss from an investment relative to its cost.
capital adequacy|Whether a financial institution has enough regulatory capital for its risks.
nonperforming loan|A loan with overdue payments or other signs of impaired repayment.
loan loss provision|An expense recorded for expected losses on loans.
deposit insurance|A scheme protecting eligible bank depositors up to set limits.
reserve requirement|The minimum reserves a bank is required to maintain.
'''
def table(src):
 out={}
 for l in src.strip().splitlines():
  if not l.strip():continue
  k,v=l.split('|',1);assert k not in out,k;out[k.strip()]=v.strip()
 return out
G=table(GENERAL);F=table(FINANCE)
vp=D/'data'/'vocabulary.json';vocab=json.loads(vp.read_text())
missing=[]
for v in vocab:
 mapping=G if v['category']=='general' else F
 if v['word'] in mapping:v['definition']=mapping[v['word']]
 else:missing.append(v['word'])
assert not missing,('Missing definitions: '+str(missing))
vp.write_text(json.dumps(vocab,ensure_ascii=False,indent=2))
print('English definitions:',len(G),'general +',len(F),'finance =',len(vocab))

# Editorial utility order: conversational usefulness first, followed by broad academic vocabulary.
# It is NOT a published corpus frequency rank.
priority="""overwhelmed acknowledge appreciate crucial outcome perspective reluctant figure out maintain consistent assume assumption emphasize apparent relevant genuine significant ensure accomplish evaluate anticipated anticipate integrate assess enhance obtain encounter overlook prioritize investigate subtle skeptical compelling plausible clarify equivalent transparent persuade awareness inevitable nuanced nuance insightful insight profound reinforce sustain resolve articulate justify mitigate sophisticated distinct evaluate interpret limitation diverse concrete concise scarce perspective retain credibility credible""".split()
rank={w:i for i,w in enumerate(priority)}
for v in vocab:
 if v['category']=='general':v['priority']=rank.get(v['word'],200+v['priority'])
 else:v['priority']=500+v['priority']
vocab.sort(key=lambda x:(x['priority'],x['word']))
vp.write_text(json.dumps(vocab,ensure_ascii=False,indent=2))
