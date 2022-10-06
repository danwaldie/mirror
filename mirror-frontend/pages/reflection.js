import Head from 'next/head'
import { useState, useEffect } from 'react';

export default function Reflection() {
    const [prompt, setPrompt] = useState('');

    useEffect(() => {
        async function fetchPrompt() {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/prompts/today/`);
            const json = await res.json();
            console.log(json)
            setPrompt(json);
        }
        fetchPrompt();
    }, [])

    return (
        <div>
            <Head>
                <title>Mirror</title>
            </Head>
            <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
                <h3 className="text-lg font-medium leading-6 text-gray-900">Today's Prompt</h3>
                <p className="mt-1 text-sm text-gray-500">
                    {prompt.prompt_text}
                </p>
            </div>
        </div>
    )
}
