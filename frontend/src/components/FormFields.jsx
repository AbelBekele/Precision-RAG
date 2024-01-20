import React from 'react'

const FormFields = ({
    labelName,
    type,
    name,
    placeholder,
    value,
    handleChange,
    isSurpriseMe,
    handleSurpriseMe,
}) => {
    return (
        <div>
            <div className="flex items-center gap-2 mb-2">
                <label className="block font-medium text-[#666e75] text-sm" htmlFor={name}>
                    {labelName}
                </label>
                {isSurpriseMe && (
                    <button onClick={handleSurpriseMe} className="py-1 px-2 bg-darkgrey text-gray-500 text-[10px]  font-medium rounded-[5px]" type='button'>
                        Generate me
                    </button>
                )}
            </div>
            <input className="w-full px-4 py-2 border border-darkgrey rounded-[5px] focus:outline-none bg-darkgrey focus:border-darkgrey text-sm" type={type} id={name} name={name} placeholder={placeholder} value={value} required onChange={handleChange} />
        </div>
    )
}

export default FormFields