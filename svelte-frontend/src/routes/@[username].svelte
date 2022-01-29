<!-- These are the user profiles! -->
<!-- Example URL: https://currencything.com/@Sam -->

<!-- Server Side Rendering! -->
<script context='module'>
    // This query is run before the page is rendered
    export async function load({url, params}) {
        // console.log(url)
        // console.log(params)
        const user = params.username
        const data = `this is the user profile of ${user}`

        // fetching the User's Blockchain data as JSON before rendering the page
        let res = await fetch('http://localhost:3000/api/blockchain/@' + user)
        let trades  = await res.json()

        return {props: {data, user, trades}}
    }
</script>

<!-- Regular client side JS -->
<script>
    export let data
    export let user
    export let trades

    import Blockchain from "../components/Blockchain.svelte"
</script>


<!-- HTML -->
<h1>{data}</h1>
<p style="text-align: center;">Welcome to {user}'s currency thing page!</p>

<Blockchain table_data={trades} />

<!-- <Blockchain /> -->