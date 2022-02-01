// # Returns an object of Blockchain Statistics for the given time period (if any)
// Takes in a query parameter called 'period'.
// How to use query parameters -> https://stackoverflow.com/questions/69370264/how-to-pass-props-to-a-sveltekit-endpoint
export async function get({url, params}) {
    const period = url.searchParams.get('period')

    const URL = `http://localhost:5000/blockchain/stats?period=${period}`
    const res = await fetch(URL)
    const data = await res.json()

    return {
        status: 200,
        body: data
    }
}