#!/usr/bin/env python3
"""Curated US-English context examples. Original sentences, independent editorial review pending.
Run repeatedly without duplicating existing examples. The first sentence becomes the canonical
cloze/quiz example. Do not infer CEFR certification or review sign-off from these additions.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# TERM | contextual sentence. Sentence must illustrate the TERM's financial/accounting sense.
FINANCE = '''
liquidity | The fund kept extra cash to maintain liquidity during volatile markets.
solvency | The lender questioned the company's solvency after three years of losses.
leverage ratio | The bank reduced its leverage ratio by raising additional equity capital.
debt-to-equity ratio | A high debt-to-equity ratio can make a company vulnerable to rising rates.
interest coverage ratio | The analyst used the interest coverage ratio to assess debt affordability.
capital structure | Management changed the capital structure by issuing new shares instead of borrowing.
equity financing | The startup chose equity financing to avoid fixed loan payments.
debt financing | Debt financing let the company expand without selling ownership stakes.
bond yield | The bond yield rose after investors sold government debt.
coupon rate | The bond's coupon rate remained fixed even when market interest rates increased.
face value | At maturity, the issuer repays the bond's face value unless it defaults.
maturity date | Her Treasury note has a maturity date in December 2028.
yield to maturity | The yield to maturity accounts for a bond's price and remaining payments.
credit spread | The credit spread widened when investors grew concerned about default risk.
credit rating | The company's credit rating fell after it took on more debt.
creditworthiness | The bank checked the borrower's creditworthiness before approving the loan.
default risk | Investors demanded a higher return to compensate for default risk.
counterparty risk | The trader limited counterparty risk by clearing the transaction through an exchange.
market risk | Diversification can reduce some risks, but it cannot eliminate market risk.
operational risk | A failed payment system exposed the firm to operational risk.
systemic risk | Regulators feared that one large bank's collapse could create systemic risk.
risk appetite | The board lowered its risk appetite after the unexpected losses.
risk tolerance | A retiree's risk tolerance may differ from that of a younger investor.
risk-adjusted return | The strategy had lower raw profits but a better risk-adjusted return.
volatility | Increased volatility made the stock's daily price swings harder to predict.
standard deviation | A higher standard deviation indicates greater dispersion in the recorded returns.
correlation coefficient | The correlation coefficient was close to zero, suggesting little linear relationship.
portfolio diversification | Portfolio diversification reduced the investor's dependence on one industry.
asset allocation | Her asset allocation shifted toward bonds as retirement approached.
rebalancing | Rebalancing restored the portfolio's target mix after stocks rallied.
benchmark index | The fund manager compared annual performance with a benchmark index.
index fund | An index fund aims to track a market index rather than select individual winners.
exchange-traded fund | She bought an exchange-traded fund through her brokerage account.
mutual fund | The mutual fund disclosed its holdings in its latest report.
expense ratio | A lower expense ratio means a smaller portion of the fund is spent on operating costs.
net asset value | The fund calculated its net asset value after markets closed.
market capitalization | The company's market capitalization doubled as its share price climbed.
price-to-earnings ratio | The price-to-earnings ratio looked unusually high relative to peers.
price-to-book ratio | Investors compared the bank's price-to-book ratio with those of similar lenders.
earnings per share | Earnings per share improved despite flat total revenue.
dividend payout ratio | The dividend payout ratio rose because the company distributed more of its earnings.
dividend yield | The dividend yield increased when the share price declined.
free cash flow | The business used free cash flow to reduce debt and repurchase shares.
discounted cash flow | The analyst used discounted cash flow to estimate the firm's value today.
net present value | The project had a positive net present value under the base-case assumptions.
internal rate of return | Management compared each project's internal rate of return with its cost of capital.
weighted average cost of capital | The valuation was sensitive to changes in the weighted average cost of capital.
cost of equity | The cost of equity increased as investors demanded a higher return.
cost of debt | Refinancing at lower rates would reduce the company's cost of debt.
terminal value | Terminal value represented most of the estimated value in the model.
discount rate | A higher discount rate lowered the present value of future cash flows.
perpetuity | The model treated the annual payment as a perpetuity with no stated end date.
annuity | The pension offered an annuity that paid a fixed amount each month.
compounding | Monthly compounding increased the account balance over several years.
compound interest | Compound interest allows previously earned interest to generate more interest.
simple interest | The short-term loan used simple interest on the original amount borrowed.
principal | Each monthly payment reduced a portion of the loan's principal.
collateral | The lender accepted the delivery truck as collateral for the business loan.
margin call | A sudden price drop triggered a margin call that required additional funds.
short selling | Short selling exposes traders to potentially unlimited losses if prices rise.
long position | She held a long position because she expected the stock to appreciate.
short position | The fund closed its short position after the company reported strong earnings.
stop-loss order | A stop-loss order can trigger after a price threshold, but execution prices may vary.
limit order | He placed a limit order to avoid paying more than his chosen price.
market order | A market order generally prioritizes execution over a guaranteed price.
bid-ask spread | The bid-ask spread widened when trading volume fell.
order book | The order book showed more buyers waiting below the current price.
liquidity provider | A liquidity provider posted buy and sell quotes throughout the session.
market maker | The market maker quoted both a bid price and an asking price.
arbitrage | The trader attempted arbitrage after spotting a temporary price difference.
hedging | The airline used fuel hedging to reduce exposure to sharp price increases.
derivative | A futures contract is a derivative whose value depends on an underlying asset.
futures contract | The farmer sold a futures contract to lock in a price for next season's harvest.
forward contract | The importer signed a forward contract to fix the dollar exchange rate.
option premium | The buyer paid an option premium for the right to purchase shares later.
strike price | The call option's strike price was below the stock's current market price.
call option | A call option gives its buyer the right, but not the obligation, to buy the underlying asset.
put option | She purchased a put option to protect against a decline in share prices.
intrinsic value | A call option has intrinsic value when the market price exceeds its strike price.
time value of an option | The time value of an option generally decreases as expiration approaches.
implied volatility | Higher implied volatility often makes options more expensive, all else equal.
beta coefficient | The stock's beta coefficient suggested greater sensitivity to market movements.
alpha | The manager claimed positive alpha after adjusting returns for market exposure.
sharpe ratio | The portfolio's sharpe ratio improved when its volatility declined.
maximum drawdown | The maximum drawdown measured the largest peak-to-trough loss in the period.
capital gain | She reported a capital gain after selling the shares above their purchase price.
realized gain | Selling the appreciated stock turned a paper profit into a realized gain.
unrealized gain | The investor's unrealized gain could disappear if prices dropped before sale.
inflation rate | The inflation rate slowed even though consumer prices continued to rise.
real interest rate | The real interest rate adjusts a nominal rate for inflation.
nominal interest rate | The bank advertised a nominal interest rate without adjusting for inflation.
yield curve | The yield curve plotted Treasury yields across different maturities.
inverted yield curve | An inverted yield curve appeared when short-term yields exceeded long-term yields.
monetary policy | The central bank tightened monetary policy to address persistent inflation.
fiscal policy | A change in taxes and government spending is an example of fiscal policy.
quantitative easing | During quantitative easing, the central bank purchased financial assets.
central bank reserves | Banks held central bank reserves to settle payments and meet liquidity needs.
foreign exchange rate | The foreign exchange rate changed before the importer paid its supplier.
currency depreciation | Currency depreciation made imported equipment more expensive in local terms.
currency appreciation | Currency appreciation made foreign vacations cheaper for domestic travelers.
balance of payments | The balance of payments records a country's transactions with the rest of the world.
current account deficit | A current account deficit can reflect spending abroad that exceeds current receipts.
sovereign debt | Investors questioned the sustainability of the country's sovereign debt.
investment-grade bond | An investment-grade bond generally carries a higher credit rating than a speculative-grade bond.
high-yield bond | The high-yield bond paid more interest in exchange for greater credit risk.
junk bond | A junk bond may offer attractive yields but carries substantial default risk.
securitization | Through securitization, the lender pooled loans into securities for investors.
asset-backed security | The asset-backed security was supported by payments on auto loans.
mortgage-backed security | A mortgage-backed security receives cash flows from a pool of mortgages.
initial public offering | The firm raised capital through an initial public offering on the stock exchange.
secondary offering | The public company announced a secondary offering of additional shares.
underwriting | The investment bank handled underwriting for the new corporate bond issue.
venture capital | The company sought venture capital to finance its early expansion.
private equity | The private equity fund acquired a controlling stake in the business.
seed funding | The founders used seed funding to build the first version of their product.
capital raise | The board approved a capital raise to fund its new manufacturing plant.
valuation multiple | The acquisition price implied a higher valuation multiple than comparable deals.
enterprise value | Enterprise value incorporates equity value and certain debt and cash adjustments.
mergers and acquisitions | Her team advises clients on mergers and acquisitions across the technology sector.
due diligence | Buyers conducted due diligence before signing the acquisition agreement.
goodwill impairment | The acquisition performed poorly, prompting the company to assess goodwill impairment.
liquidation | During liquidation, the company sold its remaining assets to repay creditors.
bankruptcy | The retailer filed for bankruptcy after it could no longer meet its obligations.
restructuring | The airline announced a restructuring aimed at reducing long-term costs.
covenant | A loan covenant required the borrower to maintain a minimum interest coverage ratio.
debt service | The lender checked whether cash flow could cover annual debt service.
refinancing | Refinancing the mortgage reduced the borrower's monthly interest expense.
loan-to-value ratio | The loan-to-value ratio fell as the homeowner paid down the mortgage.
amortization schedule | The amortization schedule showed how each payment reduced interest and principal.
balloon payment | The borrower faced a large balloon payment at the end of the loan term.
prepayment penalty | Paying off the mortgage early could trigger a prepayment penalty.
escrow account | Property taxes were collected monthly and held in an escrow account.
fiduciary duty | The adviser had a fiduciary duty to act in the client's best interest.
compliance risk | Weak internal procedures increased the firm's compliance risk.
financial statement analysis | Financial statement analysis revealed declining margins despite rising sales.
sensitivity analysis | Sensitivity analysis showed how the valuation changed with different growth rates.
scenario analysis | Scenario analysis compared the effect of a recession and a rapid recovery.
stress testing | The bank used stress testing to model losses in a severe downturn.
forecast accuracy | The analyst measured forecast accuracy by comparing projections with actual results.
cash burn rate | The startup's cash burn rate increased after it hired ten engineers.
cash runway | At its current spending rate, the company had six months of cash runway.
customer acquisition cost | The company lowered customer acquisition cost by improving referrals.
lifetime value | The team compared customer lifetime value with the cost of acquiring users.
unit economics | Healthy unit economics required the sale price to exceed the incremental service cost.
revenue growth | Revenue growth slowed when demand weakened in the second quarter.
profit margin | The firm's profit margin improved after it reduced shipping expenses.
return on equity | Return on equity increased partly because the company used more leverage.
return on assets | The bank tracked return on assets to assess how efficiently it used its balance sheet.
return on investment | The campaign's return on investment was positive after accounting for its costs.
capital adequacy | Regulators reviewed the bank's capital adequacy during the annual examination.
nonperforming loan | The bank classified the overdue commercial loan as a nonperforming loan.
loan loss provision | The lender increased its loan loss provision as borrowers showed signs of distress.
deposit insurance | Deposit insurance protects eligible deposits up to applicable coverage limits.
reserve requirement | The central bank changed the reserve requirement for certain deposit accounts.
'''
ACCOUNTING = '''
accounts payable | The company recorded the supplier's unpaid invoice in accounts payable.
accounts receivable | Accounts receivable grew when more customers bought goods on credit.
accrual accounting | Under accrual accounting, the company recognized revenue when it earned it.
cash accounting | With cash accounting, the freelancer recorded income when the payment arrived.
accrued expense | The accountant recorded an accrued expense for wages earned but not yet paid.
accrued revenue | The firm recognized accrued revenue for services delivered before invoicing.
accrued interest | The balance sheet included accrued interest on the outstanding loan.
adjusting entry | The controller posted an adjusting entry for the month's unpaid utilities.
amortization | The company recorded amortization of a patent over its useful life.
asset impairment | Management evaluated asset impairment after the factory lost a major customer.
allowance for doubtful accounts | The allowance for doubtful accounts reflected expected credit losses on receivables.
accounts aging | The accounts aging report showed which customer invoices were more than 90 days overdue.
accounting period | The accountant assigned the invoice to the correct accounting period.
accounting policy | The company disclosed its inventory valuation method as an accounting policy.
audit trail | The audit trail showed who changed the invoice and when.
auditor's opinion | Investors read the auditor's opinion before reviewing the annual statements.
balance sheet | The balance sheet listed the company's assets, liabilities, and equity.
bank reconciliation | The bookkeeper completed a bank reconciliation to explain an outstanding check.
book value | The machine's book value fell after several years of depreciation.
capital expenditure | Buying a new delivery van was recorded as a capital expenditure.
cash equivalents | The company held cash equivalents that could be converted quickly into cash.
cash flow statement | The cash flow statement explained why cash fell despite a profitable year.
chart of accounts | The controller added a new expense category to the chart of accounts.
closing entry | At year-end, the accountant posted a closing entry to clear temporary accounts.
contra asset | Accumulated depreciation is a contra asset that reduces a related asset's carrying amount.
cost allocation | The finance team used cost allocation to assign shared rent to each department.
cost of goods sold | Cost of goods sold rose when material prices increased.
credit memo | The supplier issued a credit memo for the damaged merchandise.
current asset | Inventory is normally a current asset for a retailer.
current liability | The loan payment due next month was classified as a current liability.
debit balance | After the adjustment, the cash account still showed a debit balance.
deferred expense | The prepaid annual insurance was treated as a deferred expense until recognized.
deferred revenue | The annual subscription payment created deferred revenue before the service was provided.
depletion | The mining company recognized depletion as it extracted mineral reserves.
depreciation | The company recorded depreciation on its trucks over their estimated useful lives.
direct cost | The flour used to make bread was a direct cost of production.
double-entry bookkeeping | Double-entry bookkeeping records corresponding debits and credits for each transaction.
earnings before interest and taxes | Earnings before interest and taxes increased even though interest expense rose.
expense recognition | Expense recognition required the company to record costs in the appropriate period.
fair value | The investment's fair value changed as market prices moved.
fiscal year | The organization changed its fiscal year to end in September.
fixed asset | The new manufacturing machine was classified as a fixed asset.
general ledger | The accountant traced the expense from the invoice to the general ledger.
goodwill | The buyer recognized goodwill after paying more than the fair value of identifiable net assets.
gross margin | Gross margin fell when the cost of raw materials increased.
gross profit | Gross profit equals revenue less the cost of goods sold.
historical cost | The land remained recorded at historical cost under the applicable accounting policy.
income statement | The income statement showed sales, expenses, and net income for the quarter.
indirect cost | Office rent was an indirect cost rather than a direct production expense.
intangible asset | The acquired trademark was reported as an intangible asset.
inventory turnover | Inventory turnover improved after the store reduced excess stock.
journal entry | Each journal entry included the affected accounts and amounts.
liability | An unpaid tax bill created a liability for the business.
long-term liability | The bond due in five years was reported as a long-term liability.
management accounting | Management accounting helped department leaders compare costs with budgets.
matching principle | The matching principle helps explain why related costs are recognized alongside revenue.
materiality | The auditor considered materiality when deciding which errors required correction.
net income | Net income increased after operating expenses declined.
net loss | The company reported a net loss despite higher revenue.
noncurrent asset | The factory building was classified as a noncurrent asset.
operating expense | The monthly office rent was an operating expense.
operating income | Operating income excluded the company's interest expense and taxes.
outstanding invoice | The collections team followed up on an outstanding invoice from June.
payroll expense | Payroll expense included wages and related employer costs.
prepaid expense | The annual insurance payment was recorded as a prepaid expense.
provision | The company recognized a provision for a probable obligation when the criteria were met.
purchase order | The purchasing department issued a purchase order for 200 replacement parts.
reconciliation | The accountant performed a reconciliation between the ledger and bank statement.
retained earnings | Profits kept in the company increased retained earnings.
revenue recognition | The accountant applied revenue recognition rules when the service was transferred.
sales return | The damaged item led to a sales return and a refund for the customer.
shareholders' equity | Shareholders' equity represented the residual interest after deducting liabilities.
straight-line depreciation | Straight-line depreciation spread the equipment's depreciable amount evenly over its useful life.
subsidiary ledger | The accounts receivable subsidiary ledger listed balances for individual customers.
tangible asset | A delivery truck is a tangible asset because it has physical substance.
tax liability | The year-end estimate included a tax liability for income taxes owed.
trial balance | The trial balance showed equal debit and credit totals before adjustments.
unearned revenue | Advance customer payments remained unearned revenue until earned.
variable cost | Packaging was a variable cost that rose with the number of units shipped.
variance analysis | Variance analysis explained why actual labor costs exceeded the budget.
working capital | Working capital fell after the company used cash to repay suppliers.
write-down | The damaged inventory required a write-down to its lower recoverable value.
write-off | The business approved a write-off for an account considered uncollectible.
withholding tax | The employer deducted withholding tax from the employee's paycheck.
break-even point | The store reached its break-even point after selling 800 items.
contribution margin | The contribution margin per unit helped the team estimate break-even sales.
cost center | The finance team treated the support department as a cost center.
profit center | Each regional branch was assessed as a separate profit center.
budget variance | The manager investigated a budget variance in marketing expenses.
operating budget | The annual operating budget included planned salaries, rent, and utilities.
capital budgeting | Capital budgeting helped executives decide whether to buy a new machine.
absorption costing | Under absorption costing, inventory included allocated manufacturing overhead.
activity-based costing | Activity-based costing traced overhead to the activities that caused it.
standard costing | The plant used standard costing to compare expected and actual production costs.
period cost | Advertising was treated as a period cost rather than part of inventory.
product cost | Direct materials were included in the product cost of each unit.
sunk cost | The money already spent on the failed prototype was a sunk cost.
opportunity cost | The opportunity cost of the investment was the return available elsewhere.
contingent liability | The pending lawsuit could create a contingent liability requiring disclosure.
subsequent event | The auditor assessed whether the subsequent event affected the year-end statements.
internal control | Requiring approval for large payments was an internal control.
segregation of duties | Segregation of duties prevented one employee from both approving and recording a payment.
material misstatement | The auditor identified a material misstatement in reported revenue.
asset turnover | Asset turnover measured sales generated relative to average assets.
quick ratio | The quick ratio excluded inventory when assessing short-term liquidity.
current ratio | The current ratio compared current assets with current liabilities.
receivables turnover | Receivables turnover slowed as customers took longer to pay.
days sales outstanding | Days sales outstanding increased when collections became less efficient.
inventory write-down | Unsellable products required an inventory write-down.
impairment loss | The accounting team recorded an impairment loss after testing the asset's value.
lease liability | The company reported a lease liability for future lease payments.
right-of-use asset | The office lease created a right-of-use asset under the applicable rules.
finance lease | The transaction met the criteria for a finance lease under US GAAP.
operating lease | The company classified the office rental as an operating lease under US GAAP.
consolidated statements | The parent prepared consolidated statements including its controlled subsidiaries.
noncontrolling interest | The report presented noncontrolling interest separately within equity.
intercompany transaction | The group eliminated the intercompany transaction in consolidation.
foreign exchange gain | A stronger dollar produced a foreign exchange gain on the payable in the example.
foreign exchange loss | The exchange-rate change led to a foreign exchange loss on the receivable.
stock-based compensation | The company reported stock-based compensation as part of employee expenses.
financial instrument | The company classified the swap as a financial instrument subject to disclosure.
hedge accounting | The firm assessed whether its derivatives qualified for hedge accounting.
cash-generating unit | In the impairment review, management identified the relevant cash-generating unit.
segment reporting | Segment reporting showed results for the company's retail and wholesale businesses.
related-party transaction | The audit committee reviewed the related-party transaction for proper disclosure.
financial disclosure | The financial disclosure explained the assumptions behind the impairment estimate.
restatement | The company issued a restatement to correct an error in its prior financial statements.
closing balance | The closing balance at December 31 became the next period's opening amount.
opening balance | The opening balance agreed with the previous year's closing balance.
cost basis | The investor recorded the shares' cost basis to help calculate a future taxable gain.
'''
# Carefully differentiated second examples: new situations, not a shuffled synonym of the first.
MORE = '''
liquidity | When customers requested withdrawals, the bank needed sufficient liquidity to meet them.
solvency | A firm may have enough cash for this month and still face long-term solvency problems.
leverage ratio | Regulators monitor the leverage ratio to limit excessive balance-sheet exposure.
credit spread | A narrower credit spread often signals that investors demand less compensation for credit risk.
volatility | The trader avoided making decisions based on one day of high volatility.
asset allocation | The adviser recommended reviewing asset allocation after a major life change.
rebalancing | Automatic rebalancing can reduce the temptation to chase recent market winners.
expense ratio | Even a small difference in expense ratio can affect long-term fund returns.
free cash flow | Investors examined whether free cash flow was sufficient to support dividends.
net present value | A negative net present value prompted the firm to reject the proposal.
compound interest | Starting early gives compound interest more time to work.
principal | The borrower paid interest on the remaining principal each month.
collateral | The bank could seize the collateral if the borrower defaulted, subject to the loan terms.
margin call | The investor had to deposit more cash to satisfy the margin call.
market order | During fast trading, a market order may execute at a worse price than expected.
limit order | The investor's limit order remained unfilled when the market never reached the target price.
hedging | Hedging reduced exposure to exchange-rate changes but also added costs.
call option | The call option expired worthless because the stock price stayed below the strike price.
put option | A put option can gain value as the underlying share price falls.
yield curve | Economists tracked changes in the yield curve across several months.
monetary policy | An interest-rate increase is one tool available in monetary policy.
initial public offering | The initial public offering allowed early investors to sell some of their shares.
due diligence | The buyer's due diligence uncovered a contract dispute before the deal closed.
cash runway | The founders extended their cash runway by postponing nonessential hiring.
return on investment | A positive return on investment does not necessarily mean a project had low risk.
accounts payable | Delaying accounts payable may preserve cash but strain supplier relationships.
accounts receivable | The bookkeeper followed up on accounts receivable that were past due.
accrual accounting | Accrual accounting can show a profit even when customer cash has not arrived.
balance sheet | The company's balance sheet became stronger after it paid down debt.
bank reconciliation | An unrecorded service fee was discovered during the bank reconciliation.
cash flow statement | Investors checked the cash flow statement to understand operating cash generation.
chart of accounts | A clear chart of accounts makes monthly reporting more consistent.
cost of goods sold | The retailer's cost of goods sold reflected inventory purchased and sold during the period.
current asset | Cash and short-term receivables typically qualify as current asset categories.
depreciation | Depreciation reduced accounting profit without causing a current-period cash outflow.
general ledger | The general ledger contained the transactions supporting the reported balances.
gross margin | Management compared gross margin across its product lines.
income statement | A rising sales figure on the income statement did not guarantee positive cash flow.
net income | A one-time gain boosted net income even though core operations were weaker.
prepaid expense | The prepaid expense was recognized gradually as the coverage period passed.
reconciliation | Monthly reconciliation helps identify duplicate or missing transactions.
revenue recognition | Premature revenue recognition can overstate reported sales.
retained earnings | Dividends reduced retained earnings even though the company was profitable.
trial balance | A balanced trial balance does not prove that every journal entry is correct.
working capital | Improving collections helped increase working capital.
write-off | The write-off removed the uncollectible receivable from the books.
break-even point | A price increase could reduce the number of sales required to reach the break-even point.
sunk cost | The team ignored the sunk cost when deciding whether to continue the project.
internal control | A two-person review of bank transfers served as an additional internal control.
current ratio | A high current ratio can still hide problems if inventory cannot be sold.
lease liability | Interest and payments change the lease liability over the term.
restatement | The restatement reduced previously reported earnings.
'''
GENERAL_EXTRA = '''
overwhelmed | After the sudden move, he felt overwhelmed by everything he had to organize.
resilience | The neighborhood showed remarkable resilience after the flood.
nuance | Her raised eyebrow added a nuance that the written message could not capture.
ambiguous | The contract used ambiguous language about cancellation fees.
compelling | The documentary told a compelling story about migration.
contemplate | Before quitting, she took a weekend to contemplate her options.
underlying | The doctor looked for the underlying cause rather than treating only the symptom.
attain | It took years of practice to attain that level of skill.
genuine | She showed genuine interest in her neighbor's concerns.
scrutinize | Journalists scrutinize public statements before publishing corrections.
persist | If the symptoms persist, contact a health professional.
intricate | The detective noticed an intricate pattern on the lock.
cumulative | Small daily habits can have a cumulative effect.
advocate | Many parents advocate for safer bike lanes near schools.
benchmark | Last year's results became the benchmark for this year's performance.
interpret | It is easy to interpret silence as disagreement when someone is simply thinking.
concise | A concise answer can still include all the important details.
integrate | The program helps new students integrate into campus life.
anticipate | We did not anticipate how crowded the museum would be.
scarce | Affordable apartments became scarce near the city center.
infer | From his tone, I inferred that he was disappointed.
neglect | She neglected the garden during a particularly busy month.
mitigate | Planting trees can help mitigate the urban heat effect.
subtle | There was a subtle change in the way she greeted him.
'''
PHRASAL_EXTRA = '''
figure out | It took me a while to figure out the train schedule.
come across | I came across an old photo while cleaning the closet.
come up with | Our group came up with a solution during lunch.
deal with | How do you deal with stress before an important meeting?
get over | He is still trying to get over the disappointment.
get by | They managed to get by on one income for a year.
give up | She refused to give up even after several setbacks.
bring up | He brought up the issue at the family dinner.
point out | The guide pointed out several details we had missed.
look into | The landlord promised to look into the water leak.
turn down | She turned down the invitation because she had other plans.
put off | Don't put off that difficult conversation forever.
work out | We worked out a plan that everyone could accept.
take on | The nonprofit decided to take on two new volunteers.
carry out | The team carried out the experiment twice.
make up for | We stayed late to make up for the lost time.
set aside | Try to set aside ten minutes a day for reading.
follow through on | The city must follow through on its promise to repair the bridge.
keep up with | It's hard to keep up with all the news during an election.
catch up on | I used the weekend to catch up on my reading.
run into | We ran into heavy traffic near the airport.
end up | They ended up staying in Chicago for an extra night.
break down | The car broke down just outside the city.
back up | Remember to back up your photos before resetting the phone.
fall behind | She fell behind in class after missing a week.
cut back on | We're trying to cut back on takeout meals.
stick to | If we stick to the route, we'll arrive before sunset.
speak up | Please speak up if you can't hear the presentation.
pay off | All those practice sessions eventually paid off.
go over | Can we go over the instructions one more time?
take off | The plane took off shortly after sunrise.
'''

def parse(raw):
    result={}
    for line in raw.splitlines():
        if not line.strip():continue
        key,sep,val=line.partition(' | ')
        if not sep:raise ValueError(f'Invalid curated row: {line}')
        if key in result:raise ValueError(f'Duplicate curated key: {key}')
        result[key.strip()]=val.strip()
    return result

finance=parse(FINANCE);accounting=parse(ACCOUNTING);more=parse(MORE);general=parse(GENERAL_EXTRA);pvextra=parse(PHRASAL_EXTRA)
vp=ROOT/'data/vocabulary.json';data=json.loads(vp.read_text(encoding='utf-8'))
for category,mapping in (('finance',finance),('accounting',accounting)):
    words={v['word'] for v in data if v['category']==category}
    assert words==set(mapping),f'Missing/extra {category}: {sorted(words-set(mapping))} / {sorted(set(mapping)-words)}'
assert set(more)<=set(x['word'] for x in data)
assert set(general)<=set(x['word'] for x in data)

def add_example(v,primary=None,additional=None):
    first=primary or v['example']
    others=[]
    if additional:others.append(additional)
    if v.get('examples'):
        others += [x for x in v['examples'] if x not in (first,additional)]
    examples=list(dict.fromkeys([first]+others))
    assert all(len(x)>=20 and x[-1] in '.?!' for x in examples),v['word']
    v['example']=first
    v['examples']=examples
    v['editorialStatus']='authored_unreviewed'

for v in data:
    primary={'finance':finance,'accounting':accounting}.get(v['category'],{}).get(v['word'])
    add_example(v,primary, more.get(v['word']) or general.get(v['word']))
vp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
pp=ROOT/'data/phrasals.json';ps=json.loads(pp.read_text(encoding='utf-8'))
for p in ps:
    add_example(p,additional=pvextra.get(p['word']))
pp.write_text(json.dumps(ps,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Curated {len(finance)+len(accounting)} specialist first examples; {len(more)+len(general)+len(pvextra)} additional contexts. Total vocabulary cards {len(data)}, phrasal cards {len(ps)}.')
