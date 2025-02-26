// https://www.youtube.com/watch?v=4K33w-0-p2c   good video on xml http requests  (callbacks?)
// https://www.youtube.com/watch?v=23hrM4saaMk    rebuilding the last video with the fetch api instead (it's more modern)
// look up async/await. I *think* they're built on top of promises. They're a wrapper that makes the code more readable, yet under the hood they're still promises.
// from my 1 second google, you still write your promise, then your other function will be defined as an async function by adding it as a keyword
// in the definition, aka: "async function myFunction() { ...my code ..  await myPromise() ... my code ..  }"
// https://www.youtube.com/watch?v=AMp6hlA8xKA   using websockets instead of fetch and callbacks


import {setUpEventListeners} from './components/events.js';
import {generateDebuggerElement} from "./components/debugger.js";
import {rebuild_entire_page, refresh_data} from "./components/buttons.js";

import './components/buttons.js';  // Ensure side effects still run


async function main() {
    setUpEventListeners();
    generateDebuggerElement();

    rebuild_entire_page();
    refresh_data()
}

main().catch(console.error);
