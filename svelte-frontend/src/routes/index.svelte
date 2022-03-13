<!-- THIS IS THE HOMEPAGE OF https://currencything.com/ !!! -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({fetch}) {
        // getting the website's current domain
        const DOMAIN = import.meta.env.VITE_DOMAIN

        // fetching the Blockchain data as JSON before rendering the page
        let res = await fetch(`${DOMAIN}/api/blockchain?descending=true`)
        let blockchain  = await res.json()

        // fetching the milestones
        let res2 = await fetch(`${DOMAIN}/api/blockchain/milestones`)
        let milestones = await res2.json()

        // fetching the blockchain stats
        let res3 = await fetch(`${DOMAIN}/api/blockchain/stats`)
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

    // Imports
    import Blockchain from '../components/Blockchain.svelte'
    import CurrencyStats from '../components/CurrencyStats.svelte'
    import Meta from '../components/Meta.svelte'
</script>

<!-- HTML -->
<!-- metadata -->
<svelte:head>
    <title>Currency Thing Blockchain Explorer</title>

    <!-- preloading graph images -->
    <link rel="preload" as="image" href='/graphs/supply.svg' />
    <link rel="preload" as="image" href='/graphs/mined.svg' />
    <link rel="preload" as="image" href='/graphs/trades.svg' />
    <link rel="preload" as="image" href='/graphs/user_trades.svg' />
    <link rel="preload" as="image" href='/graphs/biggest_trade.svg' />
    <link rel="preload" as="image" href='/graphs/holders.svg' />
</svelte:head>
<!-- OpenGraph/Twitter Embed -->
<Meta />

<!-- page content -->
<h1>currency thing blockchain explorer</h1>
<a href="/about"><p style="text-align: center;">learn more about currency things</p></a>

<CurrencyStats {stats} />
<hr>

<!-- <Blockchain table_data={$blockchain} /> -->
<Blockchain table_data={blockchain} {milestones} />
