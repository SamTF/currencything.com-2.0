<!-- SSR -->
<script context="module">
    export async function load({error, status}) {
        return {props: {error, status}}
    }
</script>
<!-- JS -->
<script>
    export let error
    export let status
</script>

<!-- HTML -->
<div class="err">
    <h1>:(</h1>
    <h2>{error.message}</h2>

    {#if import.meta.env.DEV}
        <h2>{error.name} {status}</h2>
        <code>{JSON.stringify(error)}</code>
    {/if}

    {#if import.meta.env.PROD}
        <h1>YEEEEEEEE</h1>
    {/if}
</div>