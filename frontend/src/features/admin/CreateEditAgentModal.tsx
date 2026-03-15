import React, { useState, useEffect } from 'react';
import {
    Modal, ModalOverlay, ModalContent, ModalHeader,
    ModalFooter, ModalBody, ModalCloseButton,
    Button, FormControl, FormLabel, Input, Select,
    Textarea, Switch, Stack, useToast
} from '@chakra-ui/react';
import axios from 'axios';

const API_BASE = "http://localhost:8000/api/v1";

export default function CreateEditAgentModal({ isOpen, onClose, onSaved, agent }: any) {
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({ 
        nome: '', 
        departamento: 'vendas', 
        prompt_contexto: '', 
        model_name: 'qwen2.5:3b', 
        is_active: true 
    });
    const toast = useToast();

    useEffect(() => {
        if (agent) setFormData(agent);
        else setFormData({ 
            nome: '', 
            departamento: 'vendas', 
            prompt_contexto: '', 
            model_name: 'qwen2.5:3b', 
            is_active: true 
        });
    }, [agent, isOpen]);

    const handleSubmit = async () => {
        setLoading(true);
        try {
            if (agent?.id) {
                await axios.put(`${API_BASE}/admin/agents/${agent.id}`, formData);
            } else {
                await axios.post(`${API_BASE}/admin/agents`, formData);
            }
            toast({ title: "Agente Salvo", status: "success" });
            onSaved();
            onClose();
        } catch (e) {
            toast({ title: "Erro ao salvar", status: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size="xl">
            <ModalOverlay backdropFilter="blur(4px)" />
            <ModalContent borderRadius="2xl">
                <ModalHeader>{agent ? "Editar Persona" : "Nova Persona IA"}</ModalHeader>
                <ModalCloseButton />
                <ModalBody pb={6}>
                    <Stack spacing={4}>
                        <FormControl isRequired>
                            <FormLabel>Nome da Persona</FormLabel>
                            <Input 
                                placeholder="Ex: Bella Vendas"
                                value={formData.nome} 
                                onChange={(e) => setFormData({ ...formData, nome: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>Departamento</FormLabel>
                            <Select 
                                value={formData.departamento} 
                                onChange={(e) => setFormData({ ...formData, departamento: e.target.value })}
                            >
                                <option value="vendas">Vendas & Consultoria</option>
                                <option value="suporte">Suporte ao Cliente</option>
                                <option value="financeiro">Financeiro / Cobrança</option>
                            </Select>
                        </FormControl>
                        <FormControl isRequired>
                            <FormLabel>Instruções do Sistema (Prompt)</FormLabel>
                            <Textarea 
                                rows={8} 
                                placeholder="Defina como a IA deve se comportar..."
                                value={formData.prompt_contexto} 
                                onChange={(e) => setFormData({ ...formData, prompt_contexto: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Modelo Base (Ollama/OpenAI)</FormLabel>
                            <Input 
                                placeholder="Ex: qwen2.5:7b ou gpt-4o"
                                value={formData.model_name} 
                                onChange={(e) => setFormData({ ...formData, model_name: e.target.value })} 
                            />
                        </FormControl>
                        <FormControl display="flex" alignItems="center">
                            <FormLabel mb="0">Ativar Imediatamente</FormLabel>
                            <Switch 
                                colorScheme="pink"
                                isChecked={formData.is_active} 
                                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })} 
                            />
                        </FormControl>
                    </Stack>
                </ModalBody>
                <ModalFooter bg="gray.50" borderBottomRadius="2xl">
                    <Button variant="ghost" mr={3} onClick={onClose}>Cancelar</Button>
                    <Button colorScheme="pink" isLoading={loading} onClick={handleSubmit}>
                        Salvar Alterações
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
}
