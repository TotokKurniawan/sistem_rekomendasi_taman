<?php

use App\Http\Controllers\LandingController;

use Illuminate\Support\Facades\Route;


use App\Http\Controllers\RekomendasiController;

Route::get('/', [LandingController::class, 'landingpage'])->name('home');
Route::get('/about', [LandingController::class, 'About'])->name('about');
Route::get('/service', [LandingController::class, 'service'])->name('service');
Route::get('/contact', [LandingController::class, 'contact'])->name('contact');
Route::get('/rekomendasi', [LandingController::class, 'rekomendasi'])->name('rekomendasi');
Route::post('/rekomendasi/proses', [RekomendasiController::class, 'prosesRekomendasi'])->name('rekomendasi.proses');
