import React, { useState, useEffect } from 'react';
import {
    Table, Thead, Tbody, Tr, Th, Td, TableContainer,
    Button, IconButton, Badge, HStack, Text, useToast,
    Skeleton, Modal, ModalOverlay, ModalContent, ModalHeader,
    ModalFooter, ModalBody, ModalCloseButton, useDisclosure,
    VStack, Divider, Heading, Icon, Box, SimpleGrid,
    Alert, AlertIcon
} from '@chakra-ui/react';
import { Eye, Trash2, Lock, Unlock, UserCheck } from 'lucide-react';
import axios from 'axios';
import CreateEditRevendedoraModal from './CreateEditRevendedoraModal';

const API_BASE = "http://localhost:8000/api/v1";

export default function AdminRevendedoras() {
    const [revendedoras, setRevendedoras] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedRev, setSelectedRev] = useState<any>(null);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const { isOpen: isAddOpen, onOpen: onAddOpen, onClose: onAddClose } = useDisclosure();
    const [summary, setSummary] = useState<any>(null);
    const [summaryLoading, setSummaryLoading] = useState(false);
    const toast = useToast();

    const fetchData = async () => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/admin/revendedoras`);
            setRevendedoras(res.data);
        } catch (error) {
            toast({ title: "Erro ao carregar representantes", status: "error" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const toggleActive = async (id: string) => {
        try {
            await axios.patch(`${API_BASE}/admin/revendedoras/${id}/toggle-active`);
            toast({ title: "Status atualizado", status: "success" });
            fetchData();
        } catch (e) {
            toast({ title: "Erro ao atualizar status", status: "error" });
        }
    }

    const deleteRev = async (id: string) => {
        if (!confirm("Excluir permanentemente este representante? Esta ação não pode ser desfeita.")) return;
        try {
            await axios.delete(`${API_BASE}/admin/revendedoras/${id}`);
            toast({ title: "Representante excluído", status: "success" });
            fetchData();
        } catch (e) {
            toast({ title: "Erro ao excluir", status: "error" });
        }
    }

    const handleAssumeProfile = async (rev: any) => {
        setSelectedRev(rev);
        setSummaryLoading(true);
        onOpen();
        try {
            const res = await axios.get(`${API_BASE}/admin/revendedoras/${rev.id}/summary`);
            setSummary(res.data);
        } catch (e) {
            toast({ title: "Erro ao carregar resumo", status: "error" });
        } finally {
            setSummaryLoading(false);
        }
    }

    return (
        <VStack align="stretch" spacing={6}>
            <HStack justify="space-between">
                <Heading size="md">Gestão de Representantes</Heading>
                <Button leftIcon={<UserCheck size={18} />} colorScheme="pink" onClick={onAddOpen}>
                    Novo Representante
                </Button>
            </HStack>
            {loading ? <Skeleton h="200px" borderRadius="2xl" /> : (
                <TableContainer bg="white" p={4} borderRadius="2xl" shadow="sm" border="1px solid" borderColor="gray.100">
                    <Table variant="simple">
                        <Thead>
                            <Tr>
                                <Th>Representante</Th>
                                <Th>WhatsApp</Th>
                                <Th>Plano</Th>
                                <Th>Status</Th>
                                <Th>Ações</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {revendedoras.map(r => (
                                <Tr key={r.id} _hover={{ bg: "gray.50" }}>
                                    <Td fontWeight="600">
                                        <VStack align="start" spacing={0}>
                                            <Text>{r.nome}</Text>
                                            <Text fontSize="xs" color="gray.400">{r.id.substring(0, 8)}...</Text>
                                        </VStack>
                                    </Td>
                                    <Td fontSize="sm">{r.telefone}</Td>
                                    <Td><Badge colorScheme="pink" borderRadius="full" px={2}>{r.plano}</Badge></Td>
                                    <Td>
                                        <Badge colorScheme={r.is_active ? "green" : "red"} borderRadius="full" px={2}>
                                            {r.is_active ? "Ativo" : "Bloqueado"}
                                        </Badge>
                                    </Td>
                                    <Td>
                                        <HStack spacing={1}>
                                            <IconButton 
                                                aria-label="Ver perfil" 
                                                icon={<Eye size={16} />} 
                                                size="sm" 
                                                variant="ghost" 
                                                onClick={() => handleAssumeProfile(r)}
                                            />
                                            <IconButton 
                                                aria-label={r.is_active ? "Bloquear" : "Desbloquear"} 
                                                icon={r.is_active ? <Lock size={16} /> : <Unlock size={16} />} 
                                                size="sm" 
                                                variant="ghost" 
                                                colorScheme={r.is_active ? "orange" : "green"}
                                                onClick={() => toggleActive(r.id)}
                                            />
                                            <IconButton 
                                                aria-label="Excluir" 
                                                icon={<Trash2 size={16} />} 
                                                size="sm" 
                                                variant="ghost" 
                                                colorScheme="red"
                                                onClick={() => deleteRev(r.id)}
                                            />
                                        </HStack>
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    </Table>
                </TableContainer>
            )}

            {/* Modal de Detalhes (Assume Profile View) */}
            <Modal isOpen={isOpen} onClose={onClose} size="xl">
                <ModalOverlay backdropFilter="blur(4px)" />
                <ModalContent borderRadius="2xl">
                    <ModalHeader borderBottom="1px solid" borderColor="gray.100">
                        <HStack justify="space-between" pr={8}>
                            <VStack align="start" spacing={0}>
                                <Text fontSize="lg">Visualização de Perfil</Text>
                                <Text fontSize="sm" fontWeight="normal" color="gray.500">{selectedRev?.nome}</Text>
                            </VStack>
                            <Badge colorScheme="purple" fontSize="xs">Modo Observador</Badge>
                        </HStack>
                    </ModalHeader>
                    <ModalCloseButton />
                    <ModalBody py={6}>
                        {summaryLoading ? <Skeleton h="200px" /> : summary && (
                            <VStack align="stretch" spacing={6}>
                                <SimpleGrid columns={2} spacing={4}>
                                    <Box p={4} bg="pink.50" borderRadius="xl">
                                        <Text fontSize="xs" color="pink.600" textTransform="uppercase">Status WhatsApp</Text>
                                        <Text fontWeight="bold">{summary.revendedora.whatsapp_status || "Desconectado"}</Text>
                                    </Box>
                                    <Box p={4} bg="blue.50" borderRadius="xl">
                                        <Text fontSize="xs" color="blue.600" textTransform="uppercase">Interações IA</Text>
                                        <Text fontWeight="bold">{summary.ai_usage} mensagens</Text>
                                    </Box>
                                </SimpleGrid>
                                
                                <Box>
                                    <Heading size="xs" mb={3} textTransform="uppercase" color="gray.500">Vendas Recentes</Heading>
                                    <VStack align="stretch" spacing={2}>
                                        {summary.recent_sales.map((v: any, i: number) => (
                                            <HStack key={i} justify="space-between" p={2} bg="gray.50" borderRadius="lg">
                                                <Text fontSize="sm" fontWeight="600">R$ {v.valor.toLocaleString('pt-BR')}</Text>
                                                <Badge size="sm" variant="subtle" colorScheme={v.status === 'confirmed' ? 'green' : 'gray'}>
                                                    {v.status}
                                                </Badge>
                                            </HStack>
                                        ))}
                                    </VStack>
                                </Box>
                                
                                <Alert status="info" borderRadius="xl" fontSize="sm">
                                    <AlertIcon />
                                    Você está visualizando os dados conforme aparecem para a representante.
                                </Alert>
                            </VStack>
                        )}
                    </ModalBody>
                    <ModalFooter bg="gray.50" borderBottomRadius="2xl">
                        <Button colorScheme="pink" leftIcon={<UserCheck size={18} />} onClick={onClose}>Entendido</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>

            <CreateEditRevendedoraModal 
                isOpen={isAddOpen} 
                onClose={onAddClose} 
                onSaved={fetchData} 
            />
        </VStack>
    );
}

