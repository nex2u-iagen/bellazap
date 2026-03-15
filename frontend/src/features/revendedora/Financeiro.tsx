import { useState } from 'react';
import {
    Box, Grid, Stat, StatLabel, StatNumber, StatHelpText,
    Button, Tabs, TabList, TabPanels, Tab, TabPanel,
    Table, Thead, Tbody, Tr, Th, Td, Badge,
    Modal, ModalOverlay, ModalContent, ModalHeader,
    ModalBody, ModalCloseButton, useDisclosure, Input,
    useToast, Flex, Text, Divider
} from '@chakra-ui/react';

export function FinanceiroRevendedora() {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [saldo, setSaldo] = useState({ disponivel: 1250.50, bloqueado: 150.00 });
    const [extrato, setExtrato] = useState([
        { id: '1', created_at: new Date().toISOString(), descricao: 'Venda via PIX', valor: 88.01, tipo: 'venda' },
        { id: '2', created_at: new Date().toISOString(), descricao: 'Pedido de Saque', valor: -200.00, tipo: 'saque' }
    ]);
    const toast = useToast();

    const handleSaque = async (valor: number) => {
        try {
            // await api.requestSaque(valor);
            toast({
                title: 'Saque solicitado com sucesso!',
                description: `R$ ${valor.toFixed(2)} já está em processamento via PIX.`,
                status: 'success',
                duration: 5000
            });
            onClose();
        } catch (error) {
            toast({ title: 'Erro ao solicitar saque', status: 'error' });
        }
    };

    return (
        <Box p={6} bg="gray.50" minH="100vh">
            <Flex justifyContent="space-between" alignItems="center" mb={8}>
                <Box>
                    <Text fontSize="2xl" fontWeight="bold">Meu Financeiro</Text>
                    <Text color="gray.600">Acompanhe seu saldo e solicite saques.</Text>
                </Box>
            </Flex>

            {/* Cards de Saldo */}
            <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={6} mb={8}>
                <Stat p={6} bg="white" borderRadius="xl" shadow="sm" borderLeft="4px solid" borderLeftColor="green.400">
                    <StatLabel color="gray.600" fontSize="sm" fontWeight="bold">Saldo Disponível</StatLabel>
                    <StatNumber fontSize="4xl" color="green.600" my={2}>
                        R$ {saldo.disponivel.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </StatNumber>
                    <StatHelpText fontWeight="medium">Livre para saque imediato via PIX</StatHelpText>
                </Stat>

                <Stat p={6} bg="white" borderRadius="xl" shadow="sm" borderLeft="4px solid" borderLeftColor="blue.400">
                    <StatLabel color="gray.600" fontSize="sm" fontWeight="bold">A Receber</StatLabel>
                    <StatNumber fontSize="4xl" color="blue.600" my={2}>
                        R$ {saldo.bloqueado.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                    </StatNumber>
                    <StatHelpText fontWeight="medium">Vendas pendentes de liquidação</StatHelpText>
                </Stat>
            </Grid>

            {/* Ação de Saque */}
            <Box p={8} bg="white" borderRadius="xl" shadow="sm" textAlign="center" mb={10}>
                <Text fontSize="lg" mb={4} fontWeight="medium">Deseja transferir seu saldo para sua conta?</Text>
                <Button
                    colorScheme="green"
                    size="lg"
                    h="60px"
                    px={12}
                    onClick={onOpen}
                    isDisabled={saldo.disponivel < 10}
                    borderRadius="full"
                    shadow="md"
                    _hover={{ shadow: 'lg', transform: 'translateY(-2px)' }}
                >
                    {saldo.disponivel < 10
                        ? 'Mínimo de R$ 10,00 para saque'
                        : 'Solicitar Saque via PIX'}
                </Button>
            </Box>

            {/* Histórico e Transações */}
            <Box bg="white" p={6} borderRadius="xl" shadow="sm">
                <Tabs variant="enclosed-colored" colorScheme="blue">
                    <TabList mb={4}>
                        <Tab fontWeight="bold">Extrato Completo</Tab>
                        <Tab fontWeight="bold">Meu Estoque</Tab>
                        <Tab fontWeight="bold">Catálogo Global</Tab>
                    </TabList>

                    <TabPanels>
                        <TabPanel px={0}>
                            <Table variant="simple">
                                <Thead>
                                    <Tr>
                                        <Th>Data</Th>
                                        <Th>Descrição</Th>
                                        <Th>Valor</Th>
                                        <Th textAlign="center">Tipo</Th>
                                    </Tr>
                                </Thead>
                                <Tbody>
                                    {extrato.map(item => (
                                        <Tr key={item.id} _hover={{ bg: "gray.50" }}>
                                            <Td color="gray.500">{new Date(item.created_at).toLocaleDateString()}</Td>
                                            <Td fontWeight="medium">{item.descricao}</Td>
                                            <Td color={item.valor > 0 ? 'green.600' : 'red.600'} fontWeight="bold">
                                                {item.valor > 0 ? '+' : ''} R$ {item.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                                            </Td>
                                            <Td textAlign="center">
                                                <Badge variant="subtle" colorScheme={
                                                    item.tipo === 'venda' ? 'green' :
                                                        item.tipo === 'saque' ? 'blue' : 'gray'
                                                } py={1} px={3} borderRadius="md">
                                                    {item.tipo.toUpperCase()}
                                                </Badge>
                                            </Td>
                                        </Tr>
                                    ))}
                                </Tbody>
                            </Table>
                        </TabPanel>

                        <TabPanel px={0}>
                            <Table variant="simple">
                                <Thead>
                                    <Tr>
                                        <Th>Produto</Th>
                                        <Th>Cód (SKU)</Th>
                                        <Th>Quantidade</Th>
                                        <Th>Preço (R$)</Th>
                                        <Th textAlign="right">Ações</Th>
                                    </Tr>
                                </Thead>
                                <Tbody>
                                    <Tr>
                                        <Td fontWeight="bold">Base Líquida 30ml</Td>
                                        <Td>BE-001</Td>
                                        <Td><Badge colorScheme="green">15 unidades</Badge></Td>
                                        <Td>R$ 45,00</Td>
                                        <Td textAlign="right"><Button size="xs" colorScheme="blue">Alterar Preço</Button></Td>
                                    </Tr>
                                </Tbody>
                            </Table>
                        </TabPanel>

                        <TabPanel px={0}>
                            <Table variant="simple">
                                <Thead>
                                    <Tr>
                                        <Th>Produto</Th>
                                        <Th>Cód (SKU)</Th>
                                        <Th>Preço Sugerido</Th>
                                        <Th textAlign="right">Ações</Th>
                                    </Tr>
                                </Thead>
                                <Tbody>
                                    <Tr>
                                        <Td>Perfume Bella Night</Td>
                                        <Td>BE-012</Td>
                                        <Td>R$ 189,90</Td>
                                        <Td textAlign="right"><Button size="xs" colorScheme="green">Adicionar ao Estoque</Button></Td>
                                    </Tr>
                                </Tbody>
                            </Table>
                        </TabPanel>
                    </TabPanels>
                </Tabs>
            </Box>

            {/* Modal de Solicitação de Saque */}
            <Modal isOpen={isOpen} onClose={onClose} isCentered size="md">
                <ModalOverlay backdropFilter="blur(5px)" />
                <ModalContent borderRadius="2xl">
                    <ModalHeader fontSize="xl" fontWeight="bold" textAlign="center" pt={8}>Solicitar Saque</ModalHeader>
                    <ModalCloseButton mt={4} />
                    <ModalBody pb={10} px={8}>
                        <Box mb={6} textAlign="center">
                            <Text fontSize="sm" color="gray.500" mb={1}>Saldo Disponível</Text>
                            <Text fontSize="2xl" fontWeight="bold" color="green.600">
                                R$ {saldo.disponivel.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                            </Text>
                        </Box>

                        <Divider mb={6} />

                        <Box mb={6}>
                            <Text fontSize="sm" fontWeight="bold" mb={2}>Valor do Saque</Text>
                            <Input
                                placeholder="R$ 0,00"
                                size="lg"
                                type="number"
                                max={saldo.disponivel}
                                min={10}
                                borderRadius="xl"
                                focusBorderColor="green.400"
                            />
                        </Box>

                        <Box bg="blue.50" p={4} borderRadius="xl" mb={8}>
                            <Flex justifyContent="space-between" mb={2}>
                                <Text fontSize="xs" color="gray.600">Taxa de Operação</Text>
                                <Text fontSize="xs" fontWeight="bold" color="green.600">R$ 0,00 (Grátis via PIX)</Text>
                            </Flex>
                            <Flex justifyContent="space-between" mb={2}>
                                <Text fontSize="xs" color="gray.600">Prazo Estimado</Text>
                                <Text fontSize="xs" fontWeight="bold">Em até 1 hora</Text>
                            </Flex>
                            <Flex justifyContent="space-between">
                                <Text fontSize="xs" color="gray.600">Conta Destino</Text>
                                <Text fontSize="xs" fontWeight="bold">Chave PIX Cadastrada</Text>
                            </Flex>
                        </Box>

                        <Button
                            colorScheme="green"
                            width="100%"
                            size="lg"
                            borderRadius="xl"
                            onClick={() => handleSaque(saldo.disponivel)}
                            _hover={{ shadow: 'md' }}
                        >
                            Confirmar e Sacar Agora
                        </Button>
                        <Button variant="ghost" width="100%" mt={2} onClick={onClose} size="sm" color="gray.500">
                            Cancelar
                        </Button>
                    </ModalBody>
                </ModalContent>
            </Modal>
        </Box>
    );
}
