<!-- this is the big table contaning all the transactions in the block chain -->
<!-- ID | INPUT | SIZE | OUTPUT | EMOTE | DATE  -->

<!-- JS -->
<script>
    export let table_data = [{a: 1, b:2, c:3}, {a: 1, b:2, c:3}, {a: 1, b:2, c:3}]

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
        <!-- Looping over every data object in the table data, and creating a row for it -->
        {#each table_data as row}
            <tr>
                <!-- looping over every value in the object -->
                {#each Object.values(row) as item}
                    <!-- <td>{item}</td> -->
                    <td>{@html item}</td>
                {/each}
            </tr>
        {/each}
    </tbody>
</table>
</div>