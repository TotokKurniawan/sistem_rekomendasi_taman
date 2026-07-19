<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class DesignAdminRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'konsep' => 'required|string|max:255',
            'lahan' => 'required|string|max:255',
            'harga' => 'required|string|max:255',
            'foto' => 'required|image|mimes:jpeg,png,jpg|max:2048',
        ];
    }
}
