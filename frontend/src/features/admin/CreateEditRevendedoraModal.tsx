import React, { useState, useEffect } from 'react';
import {
    Modal, ModalOverlay, ModalContent, ModalHeader,
    ModalFooter, ModalBody, ModalCloseButton,
    Button, FormControl, FormLabel, Input, Select,
    Stack, useToast
} from '@chakra-ui/react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

export default function CreateEditRevendedoraModal({ isOpen, onClose, onSaved }: any) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({ 
        nome: '', 
        email: '', 
        cpf_cnpj: '', 
        telefone: '', 
        plano: 'basic' 
    });
    const toast = useToast();

    useEffect(() => {
        if (!isOpen) {
            setFormData({ 
                nome: '', 
                email: '', 
                cpf_cnpj: '', 
                telefone: '', 
                plano: 'basic' 
            });
        }
    }, [isOpen]);

    const handleSubmit = async () => {
        // Validação básica
        if (!formData.nome || !formData.email || !formData.cpf_cnpj || !formData.telefone) {
            toast({ title: "Preencha todos os campos obrigatórios", status: "warning" });
            return;
        }

        setLoading(true);
        try {
            await axios.post(`${API_BASE}/admin/revendedoras`, formData);
            toast({ title: "Representante Criada!", status: "success" });
            onSaved();
            onClose();
        } catch (e: any) {
            const errorMsg = e.response?.data?.detail || "Erro ao salvar";
            toast({ title: errorMsg, status: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size="xl">
            <ModalOverlay backdropFilter="blur(4px)" />
            <ModalContent borderRadius="2xl">
                <ModalHeader>Nova Representante</ModalHeader>
                <ModalCloseButton />
                <ModalBody pb={6}>
                    <Stack spacing={4}>
                        <FormControl isRequired>
                            <FormLabel>Nome Completo</FormLabel>
                            <Input 
                                placeholder="Ex: Maria Rodrigues"
                                value={formData.nome} 
                                onChange={(e) => setFormData({ ...formData, nome: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>E-mail</FormLabel>
                            <Input 
                                type="email"
                                placeholder="maria@exemplo.com"
                                value={formData.email} 
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>CPF / CNPJ</FormLabel>
                            <Input 
                                placeholder="000.000.000-00"
                                value={formData.cpf_cnpj} 
                                onChange={(e) => setFormData({ ...formData, cpf_cnpj: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>WhatsApp / Telefone</FormLabel>
                            <Input 
                                placeholder="+55 (11) 9...."
                                value={formData.telefone} 
                                onChange={(e) => setFormData({ ...formData, telefone: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>Plano</FormLabel>
                            <Select 
                                value={formData.plano} 
                                onChange={(e) => setFormData({ ...formData, plano: e.target.value })}
                            >
                                <option value="basic">Bella Basic (R$ 49,90)</option>
                                <option value="pro">Bella Pro (R$ 99,90)</option>
                                <option value="enterprise">Bella Enterprise (Custom)</option>
                            </Select>
                        </FormControl>
                    </Stack>
                </ModalBody>
                <ModalFooter bg="gray.50" borderBottomRadius="2xl">
                    <Button variant="ghost" mr={3} onClick={onClose}>Cancelar</Button>
                    <Button colorScheme="pink" isLoading={loading} onClick={handleSubmit}>
                        Cadastrar Representante
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
}
