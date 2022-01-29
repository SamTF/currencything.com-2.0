<!-- this is the big table contaning all the transactions in the block chain -->
<!-- ID | INPUT | SIZE | OUTPUT | EMOTE | DATE  -->

<!-- JS -->
<script>
    import BlockchainRow from './BlockchainRow.svelte'

    export let table_data

    let columns = Object.keys(table_data[0]) // dynamically getting the keys of the data and using that as column headers
    // const columns = ['ID', 'INPUT', 'SIZE', 'OUTPUT', 'EMOTE', 'DATE']
</script>

<!-- HTML -->
<div class="table-container">
<table class="blockchain-table">
    <!-- The Table Column Headers -->
    <thead>
        {#each columns as column}
            <th>{column}</th>
        {/each}
    </thead>

    <!-- The Table Rows -->
    <tbody>
        <!-- Creating a BlockchainRow element for each row in the data array -->
        {#each table_data as row}
            <BlockchainRow {row} />
        {/each}
    </tbody>
</table>
</div>