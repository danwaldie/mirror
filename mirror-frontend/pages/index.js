import Head from 'next/head'
import { Fragment, useState, useEffect } from 'react';
import { FaceSmileIcon as FaceSmileIconOutline, } from '@heroicons/react/24/outline'
import { Listbox, Transition } from '@headlessui/react'
import {
    FaceFrownIcon,
    FaceSmileIcon as FaceSmileIconMini,
    FireIcon,
    HandThumbUpIcon,
    HeartIcon,
    XMarkIcon,
} from '@heroicons/react/20/solid'
import { useRouter } from 'next/router';
import Image from 'next/future/image';
import backgroundImage from '../public/Mirror_Background_3.jpg';

const moods = [
    { name: 'Excited', value: 'excited', icon: FireIcon, iconColor: 'text-white', bgColor: 'bg-red-500' },
    { name: 'Loved', value: 'loved', icon: HeartIcon, iconColor: 'text-white', bgColor: 'bg-pink-400' },
    { name: 'Happy', value: 'happy', icon: FaceSmileIconMini, iconColor: 'text-white', bgColor: 'bg-green-400' },
    { name: 'Sad', value: 'sad', icon: FaceFrownIcon, iconColor: 'text-white', bgColor: 'bg-yellow-400' },
    { name: 'Thumbsy', value: 'thumbsy', icon: HandThumbUpIcon, iconColor: 'text-white', bgColor: 'bg-blue-500' },
    { name: 'I feel nothing', value: null, icon: XMarkIcon, iconColor: 'text-gray-400', bgColor: 'bg-transparent' },
]

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

async function submitReflection(body) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/reflections/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: body
    });
    return res
}

function Prompt({ prompt }) {

    return (
        <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Today&apos;s Prompt</h3>
            <p className="mt-1 text-sm text-gray-500">
                {prompt.prompt_text}
            </p>
        </div>
    )
}

function ReflectionEntry({ prompt, user, updateTodaysReflection }) {
    const [selected, setSelected] = useState(moods[5])
    const [reflection, setReflection] = useState('');
    const router = useRouter();

    function handleReflectionChange(e) {
        setReflection(e.target.value);
    }

    useEffect(() => {
        async function delayedSubmission() {
            if (user.id && sessionStorage.getItem('prompt_id') == prompt.id) {
                const body = JSON.stringify({
                    user_id: user.id,
                    prompt_id: prompt.id,
                    reflection_text: sessionStorage.getItem('reflection_text'),
                    date_submitted: sessionStorage.getItem('date_submitted'),
                    mood: sessionStorage.getItem('mood')
                })
                const res = await submitReflection(body);
                if (res.status == 200) {
                    updateTodaysReflection(JSON.parse(body));
                    sessionStorage.clear();
                } else {
                    alert('Reflection failed.')
                }
            }
        }
        delayedSubmission();
    }, [prompt, user, updateTodaysReflection])

    async function handleSubmit(e) {
        e.preventDefault();
        const current_date = new Date();
        if (user.id) {
            const body = JSON.stringify({
                user_id: user.id,
                prompt_id: prompt.id,
                reflection_text: reflection,
                date_submitted: current_date.toISOString(),
                mood: selected.value
            });
            const res = await submitReflection(body);
            if (res.status == 200) {
                updateTodaysReflection(JSON.parse(body));
            } else {
                alert('Reflection failed.')
            }
        } else {
            sessionStorage.setItem('prompt_id', prompt.id);
            sessionStorage.setItem('reflection_text', reflection);
            sessionStorage.setItem('date_submitted', current_date.toISOString());
            sessionStorage.setItem('mood', selected.value);
            router.push('login');
        }
    }

    return (
        <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
            <div className="flex items-start space-x-4">
                <div className="min-w-0 flex-1">
                    <form action="#" method="POST" onSubmit={handleSubmit}>
                        <div className="border-b border-gray-200 focus-within:border-indigo-600">
                            <label htmlFor="reflection" className="sr-only">
                                Add your reflection
                            </label>
                            <textarea
                                rows={3}
                                name="reflection"
                                id="reflection"
                                className="block w-full resize-none border-0 border-b border-transparent p-0 pb-2 focus:border-indigo-600 text-gray-900 focus:ring-0 sm:text-sm"
                                placeholder="Write your reflection..."
                                defaultValue={''}
                                onChange={handleReflectionChange}
                            />
                        </div>
                        <div className="flex justify-between pt-2">
                            <div className="flex items-center space-x-5">
                                <div className="flow-root">
                                    <Listbox value={selected} onChange={setSelected}>
                                        {({ open }) => (
                                            <>
                                                <Listbox.Label className="sr-only"> Your mood </Listbox.Label>
                                                <div className="relative">
                                                    <Listbox.Button className="relative -m-2 inline-flex h-10 w-10 items-center justify-center rounded-full text-gray-400 hover:text-gray-500">
                                                        <span className="flex items-center justify-center">
                                                            {selected.value === null ? (
                                                                <span>
                                                                    <FaceSmileIconOutline className="h-6 w-6 flex-shrink-0" aria-hidden="true" />
                                                                    <span className="sr-only"> Add your mood </span>
                                                                </span>
                                                            ) : (
                                                                <span>
                                                                    <span
                                                                        className={classNames(
                                                                            selected.bgColor,
                                                                            'flex h-8 w-8 items-center justify-center rounded-full'
                                                                        )}
                                                                    >
                                                                        <selected.icon className="h-5 w-5 flex-shrink-0 text-white" aria-hidden="true" />
                                                                    </span>
                                                                    <span className="sr-only">{selected.name}</span>
                                                                </span>
                                                            )}
                                                        </span>
                                                    </Listbox.Button>

                                                    <Transition
                                                        show={open}
                                                        as={Fragment}
                                                        leave="transition ease-in duration-100"
                                                        leaveFrom="opacity-100"
                                                        leaveTo="opacity-0"
                                                    >
                                                        <Listbox.Options className="absolute z-10 -ml-6 w-60 rounded-lg bg-white py-3 text-base shadow ring-1 ring-black ring-opacity-5 focus:outline-none sm:ml-auto sm:w-64 sm:text-sm">
                                                            {moods.map((mood) => (
                                                                <Listbox.Option
                                                                    key={mood.value}
                                                                    className={({ active }) =>
                                                                        classNames(
                                                                            active ? 'bg-gray-100' : 'bg-white',
                                                                            'relative cursor-default select-none py-2 px-3'
                                                                        )
                                                                    }
                                                                    value={mood}
                                                                >
                                                                    <div className="flex items-center">
                                                                        <div
                                                                            className={classNames(
                                                                                mood.bgColor,
                                                                                'w-8 h-8 rounded-full flex items-center justify-center'
                                                                            )}
                                                                        >
                                                                            <mood.icon
                                                                                className={classNames(mood.iconColor, 'flex-shrink-0 h-5 w-5')}
                                                                                aria-hidden="true"
                                                                            />
                                                                        </div>
                                                                        <span className="ml-3 block truncate font-medium text-gray-900">{mood.name}</span>
                                                                    </div>
                                                                </Listbox.Option>
                                                            ))}
                                                        </Listbox.Options>
                                                    </Transition>
                                                </div>
                                            </>
                                        )}
                                    </Listbox>
                                </div>
                            </div>
                            <div className="flex-shrink-0">
                                <button
                                    type="submit"
                                    className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                >
                                    Post
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

function ReflectionResponse({ todaysReflection }) {
    return (
        <div className="border-b border-gray-200 bg-white px-4 py-5 sm:px-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Your Response</h3>
            <p className="mt-1 text-sm text-gray-500">
                {todaysReflection.reflection_text}
            </p>
        </div>
    )
}

export default function Reflection() {
    const [prompt, setPrompt] = useState('');
    const [user, setUser] = useState({});
    const [todaysReflection, setTodaysReflection] = useState({});

    useEffect(() => {
        async function fetchUser() {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/me/`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            });
            const json = await res.json();
            setUser(json);
        }
        fetchUser();
    }, [])

    useEffect(() => {
        async function fetchPrompt() {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/prompts/today/`);
            const json = await res.json();
            setPrompt(json);
        }
        fetchPrompt();
    }, [])

    useEffect(() => {
        async function fetchTodaysReflection() {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/reflections/today/me/`, {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token')
                }
            });
            if (res.status == 200) {
                const json = await res.json();
                setTodaysReflection(json);
            }
        }
        fetchTodaysReflection();
    }, [])

    function updateTodaysReflection(e) {
        setTodaysReflection(e);
    }

    return (
        <div>
            <Head>
                <title>Mirror</title>
            </Head>
            <div className="relative mt-14 sm:mt-24">
                <div className="absolute inset-x-0 -top-40 -bottom-32 overflow-hidden bg-indigo-50">
                    <Image
                        className="absolute left-full top-0 -translate-x-1/2 sm:left-1/2 sm:translate-y-[-15%] sm:translate-x-[-20%] md:translate-x-0 lg:translate-x-[5%] lg:translate-y-[4%] xl:translate-y-[-8%] xl:translate-x-[27%]"
                        src={backgroundImage}
                        alt=""
                        width={918}
                        height={1495}
                        unoptimized
                    />
                    <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-white" />
                    <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-white" />
                </div>
                <div className='space-y-8 bg-white/60 py-14 px-4 sm:px-10 m-4 sm:m-16 min-w-min shadow-xl rounded-lg shadow-blue-900/5 backdrop-blur'>
                    <Prompt prompt={prompt} />
                    <div>
                        {todaysReflection.reflection_text ? (
                            <ReflectionResponse todaysReflection={todaysReflection} />
                        ) : (
                            <ReflectionEntry prompt={prompt} user={user} updateTodaysReflection={updateTodaysReflection} />
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}
