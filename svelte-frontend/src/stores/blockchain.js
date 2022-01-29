import {writable} from 'svelte/store'

export const blockchain = writable([])

const fetchBlockchain = async () => {
    const url = 'http://localhost:5000/blockchain'
    const res = await fetch(url)
    const data = await res.json()

    blockchain.set(data)
}

fetchBlockchain()