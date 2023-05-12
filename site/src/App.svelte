<script>
  import { Search, Button, Spinner } from "flowbite-svelte";
  import { sanitize } from "./lib/sanitize.js";
  import Comic from "./lib/Comic.svelte";
  import Accordian from "./Accordian.svelte";
  import { fade } from "svelte/transition";
  import { SvelteToast, toast } from "@zerodevx/svelte-toast";
  import logoSVG from "./assets/logo.svg";

  let mapURL;
  let mostRecentComicData;
  (async () => {
    mapURL = await (await fetch("/getMapURL")).text();
    const mostRecentComicID = await (
      await fetch("/getMostRecentComicID")
    ).json();
    mostRecentComicData = await (
      await fetch(`/fetchxkcd/${mostRecentComicID}`)
    ).json();
  })();

  let searchInputText;
  let searching = false;
  let resultsData = [];
  let showAmount = 5;
  async function search() {
    if (searching) return;
    resultsData = [];
    showAmount = 5;
    const sanitizedInput = sanitize(searchInputText);
    searching = true;

    const res = await fetch(`/search?q=${sanitizedInput}`);
    if (res.status === 429) {
      searching = false;
      toast.push("You have been rate limited. Please try again later!", {
        theme: {
          "--toastBarBackground": "red",
        },
      });
    } else if (res.status !== 200) {
      searching = false;
      toast.push("An unknown error has occurred. Please try again later!", {
        theme: {
          "--toastBarBackground": "red",
        },
      });
    }
    resultsData = await res.json();

    searching = false;
  }
  function showMore() {
    if (showAmount + 5 <= resultsData.length) {
      showAmount += 5;
    }
  }
</script>

<main>
  <SvelteToast />
  <a href="/"
    ><img
      src={logoSVG}
      alt="logo with Beret Guy using magnifying glass"
      class="w-28 top-2 left-2 m-auto lg:m-0 lg:absolute"
    /></a
  >
  <div>
    <a
      href="https://github.com/KDJDEV/xkcdfinder"
      class="inline-flex top-2 right-2 m-auto lg:m-0 relative lg:absolute items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        ><path
          d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
        /></svg
      >
      <span class="flex-1 ml-3 whitespace-nowrap"
        >View source code on GitHub</span
      >
    </a>
    <h1 class="mt-5">xkcdfinder</h1>
    <p>Find the perfect xkcd comic with a flexible AI search.</p>

    <form on:submit|preventDefault={search}>
      <Search bind:value={searchInputText}>
        <Button type="submit">Search</Button>
      </Search>
    </form>
    <p class=" text-gray-500">
      Be as descriptive as you like. This search isn't keyword based, but intent
      based.
    </p>
  </div>
  <div
    class="max-w-[600px] m-auto relative mt-5 text-gray-500 pt-6"
    style="margin-bottom:{resultsData.length > 0 ? '150px' : 0}"
  >
    {#if searching}
      <div in:fade class=" mt-10">
        <Spinner size="20" />
      </div>
    {/if}

    {#each resultsData.slice(0, showAmount) as result}
      <Comic id={result.id} />
    {/each}

    {#if resultsData.length > 0}
      <p class="absolute top-0 left-0 m-1">
        Results are sorted by similarity to your search
      </p>
      {#if showAmount < resultsData.length}
        <Button class="float-left" color="dark" on:click={showMore}
          >Show more comics</Button
        >
      {/if}
    {/if}
  </div>

  <div class="mt-10">
    <h2 class="text-4xl">xkcd comic visualization</h2>
    <ul class=" list-disc text-left px-5 mt-2 mb-2">
      <li>Each dot represents a comic.</li>
      <li>
        Dots close to each other should be comics that are more similar, while
        those farther apart should be less similar.
      </li>
      <li>You can see which comic any dot represents by clicking it.</li>
    </ul>
    <div class="w-full h-[400px] border-4 shadow-md">
      {#if mapURL}
        <iframe src={mapURL} title="xkcd comics" class="w-full h-full" />
      {:else}
        <div out:fade class=" mt-36">
          <Spinner size="20" />
        </div>
      {/if}
    </div>
    <p class="mt-1">
      Visualization provided by <a href="https://github.com/nomic-ai/nomic"
        >Nomic Atlas</a
      >
    </p>
  </div>

  <Accordian {mostRecentComicData} />
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
