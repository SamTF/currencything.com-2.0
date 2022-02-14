<!-- THIS IS THE HOMEPAGE OF https://currencything.com/ !!! -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({fetch}) {
        // fetching the Blockchain data as JSON before rendering the page
        let res = await fetch('http://localhost:3000/api/blockchain?descending=true')
        let blockchain  = await res.json()

        // fetching the milestones
        let res2 = await fetch('http://localhost:3000/api/blockchain/milestones')
        let milestones = await res2.json()

        // fetching the blockchain stats
        let res3 = await fetch('http://localhost:3000/api/blockchain/stats')
        let stats = await res3.json()

        if (res.ok) {
            return {props: {blockchain, milestones, stats}}
        } else {
            return {props: 'error'}
        }
    }
</script>
<!-- JS -->
<script>
    // "importing" the data from the SSR "load" function
    export let blockchain
    export let milestones
    export let stats

    // const newData = blockchain.map(row => ({...row, EMOTE: `/images/emotes/{${row.EMOTE}}.webp`}))
    // console.log(newData)

    // Imports
    import Blockchain from '../components/Blockchain.svelte'
    import CurrencyStats from '../components/CurrencyStats.svelte'
</script>

<!-- HTML -->
<!-- metadata -->
<svelte:head>
    <title>Currency Thing Blockchain Explorer</title>
    <meta name="description" content="this is the page description">
    <meta name="ass" content="yes">

    <!-- preloading graph images -->
    <link rel="preload" as="image" href='/graphs/supply.svg' />
    <link rel="preload" as="image" href='/graphs/mined.svg' />
    <link rel="preload" as="image" href='/graphs/trades.svg' />
    <link rel="preload" as="image" href='/graphs/user_trades.svg' />
    <link rel="preload" as="image" href='/graphs/biggest_trade.svg' />
    <link rel="preload" as="image" href='/graphs/holders.svg' />
</svelte:head>

<!-- page content -->
<h1>currency thing blockchain explorer</h1>
<a href="/about"><p style="text-align: center;">learn more about currency things</p></a>

<CurrencyStats {stats} />
<hr>

<!-- <Blockchain table_data={$blockchain} /> -->
<Blockchain table_data={blockchain} {milestones} />
{blockchain[0].INPUT}

<img src='/images/emotes/Sam.webp' alt="AAAAAAA">

<!-- CSS -->
