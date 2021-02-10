# Streamr Agreements

This is a simple spec as a launch point. This document considers a single agreement concerning support for a single stream.

![](agreement.png)

## State

| Name | Symbol | Definition | initial value|
| -------- | -------- | -------- | -- |
|  Allocated Funds   | $A$     | $A = \sum_{i\in \mathcal{B}} a_i$      |  0|
|  Unallocated Funds   | $R$     | $F-A$  | 140|
|  Total Funds   | $F$     |     | 140|
|  Committed Brokers |  $\mathcal{B}$ | | $\emptyset$| 
| Number of Brokers | $n$ | $n=\vert\mathcal{B}\vert$ |0|
| Broker Claimable Funds | $a_i$| | 0|
|  Broker Stake| $s_i$ |  | 5 (=$s_\min$) |
| Total Broker Stake | $S$  | $S=\sum_{i\in \mathcal{B}} s_i$|0 |
| Horizon | $H$ | $\frac{R}{\Delta A}$| 20$\left(=\frac{F}{\Delta A}\right)$

## Parameters

| Name | Symbol | Definition |  initial value|
| -------- | -------- | -------- | -- |
|  Required Stake   | $s_{\min}$     | $s_i\ge \sigma$ | 5|
| Epoch Length   | $\Delta t$     | | 1 day |
| Min Epochs | $\tau$| | 28
| Allocation Per Epoch | $\Delta A$| | 10 |
| Min Horizon | $H_{\min}$| |7|
| Min Brokers | $n_{\min}$| |1|
| Max Brokers | $n_{\max}$| |5|

## Mechanisms
![](https://i.imgur.com/12NhGZc.png)


### Owner

#### Deploy

An actor within the streamr ecosystem can deploy a new agreement contract by specifying which stream the agreement supports, setting the parameters of the smart contract providing initial funds, and providing any (unenforced) commitment to continue topping up the contract as payer under as long as a set of SLAs are met. For the purpose of this draft, it is assume that the contract is initialized with some quantity of funds $F$ such that $H>H_{\min}$ and that $\mathcal{B} = \emptyset$.

#### Cancel

In the event that the owner closes down a contract, each Broker gets back their stake, and recieves any unclaimed tokens allocated to their address as well an equal share of the remaining unallocated assets.

That is to say the quantity $\Delta d_i$ of data tokens is distributed to each broker $i \in \mathcal{B}$

$$\Delta d_i = s_i + a_i + \frac{R}{N}$$

and thus the penultimate financial state of the contract is

$$S=0\\
R = 0\\
A = 0 $$

when the contract is self-destructed.

#### Forced Cancel

There may conditions under which any address may trigger the cancel but these conditions should be indicative of a failure on the part of the payer. An example policy would be to allow forced cancel when $n < n_{\min}$ and $H<H_\min$, and possibly only if this is the case more multiple epochs.

### Payer

A payer, who may or may not be the owner may contribute funds to the agreement in order to ensure its continued existence.

#### Pay

A payer takes the action pay by providing a quantity of DATA tokens $\Delta F$ which increased the unallocated funds (and thus also the total funds).

$$ F^+ = F+\Delta F\\
R^+ = R + \Delta F$$

Furthermore, the Horizon $H$ is increased

$$ H^+ = \frac{R+\Delta F}{\Delta A} = H + \frac{\Delta F}{\Delta A}$$


### Synthetic State Change

The synthetic state change is a change the contract state that is not realized until later. In this case the automatic allocation of funds from the pool $R$ to the pool $A$ is implicit. For reference see geyser contracts, although rewards each participant is entitled to are determinstic, they are not actually resolved until they make a claim, see broker actions.

Per epoch $t$ of length $\Delta t$, let $\mathcal{B}_t$ be the set of brokers $i\in \mathcal{B}$ for the entirety of the epoch, and if $n_t= \vert \mathcal{B}_t\vert>n_\min$ then

$$a_i^+ = a_i +\frac{\Delta A}{n_t}\\
A^+ = A+\Delta A\\
R^+=R-\Delta A$$

Note that $F^+ = F$ so no tokens are actually flowing, this book-keeping reflects the amount of funds broker $i$ will recieve in the event that they make a claim or other payout event occurs. 

Furthmore, if $n_t= \vert \mathcal{B}_t\vert<n_\min$, payments are not issued as the terms of the agreement are not considered met, and additional allocations are not accrued for the passage of epoch $t$:

$$a_i^+ = a_i\\
A^+ = A\\
R^+=R$$

If having one broker suffices then setting $n_\min=1$ is recommended.

Above, I have considered a very simple conditional allocation policy, that provides a fixed reward of $\Delta A$ per epoch $\Delta t$ evenly over the brokers in the agreement as long as the minimum broker count is met. This is placeholder logic, both the total flow and the allocation rule can be state dependent. An example alternative would be to release an amount of funds which is a scale factor on the total tokens staked up to some cap: $\Delta A = \max (\gamma S, \Delta A_\max)$, where each broker received $\Delta a_i = a_i^+-a_t= \gamma s_i$ unless the cap was met.

### Broker

#### Join

A broker $i$ can join the agreement (and must also join the stream associated with that agreement) by staking $s_i\ge \sigma$

$$ \mathcal{B}^+ = \mathcal{B} \cup \{i\}\\
S^+ = S+s_i
$$

Note that if the act of joining would cause $\vert \mathcal{B}^+ \vert > n_\max$ then joining would fail. It is not possible for more than $n_\max$ brokers to be party to this agreement.

Furthermore, it is possible to enforce addition access control via whitelists or blacklists which serve to restrict access to the set $\mathcal{B}$. These lists may be managed by the owner, the payers, and/or the brokers; however, scoping an addition access control scheme is out of scope at this time.

#### Claim

A broker is attached to agreement can claim their accumulated rewards at their discretion. 

$$A^+= A-a_i \\
F^+= F-a_i$$

Note that while this decreases the total funds in the contract it does not decrease the unallocated (remaining) funds in the conract because claims only extract claims according to a deterministic rule computed over the past.

Many brokers may choose to claim their funds more or less often depending on opportunity costs and gas costs.

Preferred implementations may vary -- see section on synthetics state.

#### Leave

In the event that the horizon is below the threshold $H<H_\min$ or a broker has been attached to the agreement for more than $\tau$ epochs a broker may exit an agreement and take their stake (and outstanding claims):

$$\mathcal{B}^+ = \mathcal{B}-\{i\}\\
S^+ = S-s_i \\
A^+= A-a_i \\
F^+= F-a_i$$

The broker recieves the balance $s_i + a_i$.


However if a broker has not stayed for the entire period $\tau$ or the contract is not running low on funds, the stake will be kept as payment by the agreement contract when the broker leaves

$$\mathcal{B}^+ = \mathcal{B}-\{i\}\\
S^+ = S-s_i \\
A^+= A-a_i \\
F^+= F+s_i-a_i$$

The broker only recieves $a_i$.

In a more extreme case we may require the broker to relinquish the claim on $a_i$ as well but this would easily be skirted by making a claim action before leaving.




