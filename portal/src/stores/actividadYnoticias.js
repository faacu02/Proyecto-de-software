import { defineStore } from 'pinia';
import axios from 'axios';

const apiBaseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000/api'
    : 'https://admin-grupo20.proyecto2024.linti.unlp.edu.ar/api';

export const useActividadYNoticiasStore = defineStore('actividadYNoticias', {
    state: () => ({
        actividadYnoticias: [],
        noticia: null,
        loading: false,
        error: null,
        totalPages: null
    }),
    actions: {
        async fetchActividadYnoticias(params) {
            const { author, published_from, published_to, page, per_page } = params;
            
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get(`${apiBaseUrl}/articulo/filtrar`, {
                    params: {
                        author,
                        published_from,
                        published_to,
                        page,
                        per_page
                    }
                });
                this.actividadYnoticias = response.data.data;
                this.totalPages = response.data.cantidad_paginas;
            } catch (error) {
                this.error = 'Error al cargar las actividades y noticias';
            } finally {
                this.loading = false;
            }
        },
        async fetchNoticiaById(id) {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get(`${apiBaseUrl}/articulo/${id}`);
                this.noticia = response.data;
                return response.data;
            } catch (error) {
                this.error = 'Error al cargar la noticia';
                return null;
            } finally {
                this.loading = false;
            }
        }
    },
});