<!-- THIS IS THE HOMEPAGE OF https://currencything.com/ !!! -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({fetch}) {
        // fetching the Blockchain data as JSON before rendering the page
        let res = await fetch('http://localhost:3000/api/blockchain')
        let blockchain  = await res.json()

        if (res.ok) {
            return {props: {blockchain}}
        } else {
            return {props: 'error'}
        }
    }
</script>
<!-- JS -->
<script>
    // "importing" the data from the SSR "load" function
    export let blockchain

    // const newData = blockchain.map(row => ({...row, EMOTE: `/images/emotes/{${row.EMOTE}}.webp`}))
    // console.log(newData)

    // Imports
    import Blockchain from '../components/Blockchain.svelte'

    async function fetchBlockchain() {
        const url = 'http://localhost:3000/api/blockchain/'
        const res = await fetch(url)
        const data = await res.json()

        console.log(data)
    }

    // fetchBlockchain()
    // https://stackoverflow.com/questions/67568323/how-can-i-send-secure-api-requests-from-sveltekit-app-without-showing-api-keys
    // https://svelte.dev/repl/fdd5034d023146f49614d3b087515df5?version=3.46.2
</script>

<!-- HTML -->
<!-- metadata -->
<svelte:head>
    <title>Currency Thing Blockchain Explorer</title>
    <meta name="description" content="this is the page description">
    <meta name="ass" content="yes">
</svelte:head>

<!-- page content -->
<h1>currency thing blockchain explorer</h1>
<p>now available in svelte!</p>

<hr>

<a href="/about">learn more about currency things</a>

<hr>

<!-- <Blockchain table_data={$blockchain} /> -->
<Blockchain table_data={blockchain} />
{blockchain[0].INPUT}

<img src='/images/emotes/Sam.webp' alt="AAAAAAA">

<!-- CSS -->
