<script>
  import { Search, Button } from 'flowbite-svelte'
  import Comic from './lib/Comic.svelte';
</script>

<main>
  <h1>searchxkcd</h1>
  <p>Search for xkcd comics with flexible AI search.</p>

  <Search >
    <Button>Search</Button>
  </Search>
  <p class=" text-gray-500">Be as descriptive as you like. This search isn't keyword based, but an intent based search.</p>

  <Comic id=153/>
  <iframe src="https://atlas.nomic.ai/map/1dc681ca-f380-4524-a1db-653c51808b02/7f99ac20-5e8c-40c0-9d2e-53cf68493afa" title="xkcd comics" width="100%" height="400px"></iframe>
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
